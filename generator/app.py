import base64
import hashlib
import hmac
import json
import os
import smtplib
import time
import traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable open CORS for flexible API gateway patterns
CORS(app)

def resolve_config(var_name, default_value=None):
    """Helper function to cleanly resolve environment configurations."""
    val = os.environ.get(var_name, default_value)
    if not val:
        raise ValueError(f"Required configuration environment variable missing: {var_name}")
    return val

def create_jwt_token(email, mode, signing_key):
    """
    Pure Python JWT Engine - Cryptographically generates a short-lived
    verification artifact without forcing heavy external binary library dependencies.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    
    now = int(time.time())
    payload = {
        'email': email,
        'mode': mode,
        'iss': 'vault-system',  # Standard open-source issuer claim matching the validator
        'aud': 'vault-access',  # Standard open-source audience claim matching the validator
        'iat': now,
        'exp': now + int(5.5 * 60),  # Explicit 5.5 minute TTL enforcement
        'jti': f"{email}-{now}"
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        signing_key.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def dispatch_generic_email(recipient_email, access_url, mode):
    """
    A generic, provider-agnostic notification dispatcher using standard SMTP.
    Replaces vendor-locked APIs (like the Google Gmail API) so open-source users
    can configure dispatch parameters out-of-the-box via environment variables.
    """
    smtp_server = resolve_config("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(resolve_config("SMTP_PORT", "587"))
    sender_email = resolve_config("SENDER_EMAIL")
    sender_password = resolve_config("SENDER_PASSWORD") # App-specific token
    app_name = resolve_config("APPLICATION_NAME", "Sovereign Identity Portal")

    message = MIMEMultipart('alternative')
    message['To'] = recipient_email
    message['From'] = sender_email
    message['Subject'] = f"{app_name} - Identity Verification"
    
    # HTML Content
    body_html = f"""
    <html>
    <body>
        <h2>{app_name} - Secure Access Verification</h2>
        <p><strong>Clearance Level Request:</strong> {mode.upper()}</p>
        <p><a href="{access_url}" style="background-color: #007BFF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Verify Secure Identity</a></p>
        <p><em>Attention: This link expires in 5 minutes for perimeter integrity.</em></p>
        <p>If you did not initiate this authentication flow, please ignore this communication.</p>
    </body>
    </html>
    """
    
    # Text Fallback
    body_text = f"Clearance Level: {mode.upper()}\nAccess Link: {access_url}\nThis link expires in 5 minutes.\n\nIf you did not request this access, please ignore this email."
    
    message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))
    
    # Secure SMTP execution envelope
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/dispatch', methods=['POST'])
def handler():
    logger_name = "TokenGeneratorEngine"
    default_mode = "customer"
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Malformed request', 'message': 'Missing JSON body'}), 400

        email = data.get('email', '').lower().strip()
        if not email:
            return jsonify({'error': 'IDENT_REQUIRED', 'message': 'Identity string parameters are required.'}), 400

        # Dynamic variable configuration retrieval
        try:
            domain = resolve_config("UI_DOMAIN_URL")
            signing_key = resolve_config("VAULT_SIGNING_KEY")
        except ValueError as cfg_err:
            print(f"❌ Configuration Error: {str(cfg_err)}")
            return jsonify({'error': 'SERVER_CONFIG_ERROR', 'message': 'Generator is missing signature context.'}), 500
        
        # Mint the 5.5-minute state-isolated token
        token = create_jwt_token(email, default_mode, signing_key)
        access_url = f"{domain}/verify.html?token={token}"

        # Dispatch the verification ticket
        dispatch_generic_email(email, access_url, default_mode)
        print(f"✅ [{logger_name}] Verification token securely dispatched for identity endpoint.")

        return jsonify({'message': 'SECURE_LINK_DISPATCHED'}), 200

    except Exception as e:
        error_msg = traceback.format_exc()
        # Keep granular diagnostics tucked inside local environment container logs
        print(f"❌ [{logger_name}] Critical Exception: {str(e)}")
        print(error_msg)
        
        # Obfuscate systemic internals from downstream clients to maintain environment security
        return jsonify({
            'error': 'INTERNAL_SYSTEM_ERROR',
            'message': 'An unexpected processing failure occurred within the generator service boundary.'
        }), 500

if __name__ == "__main__":
    bind_port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=bind_port)
