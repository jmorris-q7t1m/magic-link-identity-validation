Here is the master architectural `README.md` for your repository. It frames your two-container token airlock framework with the high-level authority of your 59-paper ecosystem under the Apache 2.0 license, while keeping your proprietary dissertation mathematics completely protected.

---

# Sovereign Identity Airlock Framework

An enterprise-grade, algorithm-agnostic, token-based identity isolation and verification framework. This repository provides a stateless, two-container architecture designed to completely eliminate identity leakage (such as PII or cleartext emails) across down-stack enterprise microservice topologies.

This framework is distributed under the **Apache License 2.0**.

```
[ CLIENT ] ──(Raw Identifier)──► [ OPEN SOURCE GENERATOR ]
                                           │ (Uses Abstract Cipher/PQC)
                                           ▼
[ APPS ]   ◄───(Anonymized ID)─── [ OPEN SOURCE VALIDATOR ]
```

---

## Architectural Philosophy

Traditional enterprise authentication frameworks leak state. When microservices handle tokens containing raw, unhashed user identifiers (e.g., standard JWT claims), every single service boundary becomes a potential point of failure for identity disclosure.

The **Sovereign Identity Airlock Framework** solves this problem by enforcing a strict, deterministic, two-part microservice boundary:

1. **The Token Generator Engine (Ingress Gate):** Ingests raw identity parameters, cryptographically encapsulates them into an ephemeral, stateless token with a hard-coded 5.5-minute lifespan, and dispatches an out-of-band access ticket to the user.
2. **The Token Validator Engine (Perimeter Airlock):** Incepts the token, cryptographically verifies the signatures, and immediately processes the identity claims through a deterministic, non-reversible mathematical folding interface (`SovereignIdentityAirlock`). Downstream application logic never handles raw identifiers; they only receive a highly secure, anonymized topological handle (`folded_id`).

### Deterministic Linear Execution

To preserve strict state windows and prevent memory race conditions during cryptographic transformation, both microservices are engineered to run under a **single-worker, single-thread (`--threads 1`) Gunicorn configuration**.

This repository is built for highly scalable cloud architectures. Horizontal scaling should be handled at the **container orchestration layer** (e.g., Google Cloud Run, AWS ECS Fargate) with maximum container instance concurrency set to `1`. This guarantees absolute linear isolation for every discrete authentication execution.

---

## Repository Structure

```text
sovereign-identity-airlock/
│
├── LICENSE                  # Apache License 2.0
├── README.md                # Architectural Master Blueprint
│
├── generator/               # Token Generation & Dispatch Service
│   ├── app.py               # Sanitized Token Minter Script
│   ├── requirements.txt     # Service Dependencies
│   └── Dockerfile           # Layer-Cached Single-Threaded Container
│
└── validator/               # Perimeter Gate & Verification Service
    ├── app.py               # Sanitized Validation Script
    ├── requirements.txt     # Service Dependencies
    └── Dockerfile           # Layer-Cached Single-Threaded Container

```

---

## Core Interface: `SovereignIdentityAirlock`

The validator incorporates an inline interface blueprint called `SovereignIdentityAirlock`. It exposes a `.fold()` method signature designed to accept a string and return an anonymized identifier:

```python
class SovereignIdentityAirlock:
    def __init__(self, sovereign_string: str):
        self._secret_seed = sovereign_string.encode('utf-8')

    def fold(self, identity_raw: str) -> str:
        # Standard default: Secure symmetric HMAC-SHA256
        hashed = hmac.new(self._secret_seed, identity_raw.encode('utf-8'), hashlib.sha256).hexdigest()
        return f"v_id_{hashed[:32]}"

```

### Algorithm-Agnostic Extension

While the default implementation relies on strong symmetric hashing, the framework's interface contract is entirely algorithm-agnostic. Organizations deploying into quantum-threat environments can swap out the inner logic of the `.fold()` method to inject specialized **Post-Quantum Cryptography (PQC)** solutions—such as lattice-based ciphers or advanced asymmetric tokenization matrices—without changing a single line of the network or routing logic.

---

## Environment Configuration

Both containers are entirely stateless and depend on runtime configuration injected via environment variables.

### Generator Environment Variables

* `UI_DOMAIN_URL`: The base URL destination for your client application interface.
* `VAULT_SIGNING_KEY`: The secure secret key used to sign the outgoing token's `HS256` signature.
* `SENDER_EMAIL`: The source email address executing the notification dispatch.
* `SENDER_PASSWORD`: The secure credential or app-specific token authorizing SMTP mail relay.
* `SMTP_SERVER`: (Optional) Defaults to `smtp.gmail.com`.
* `SMTP_PORT`: (Optional) Defaults to `587`.

### Validator Environment Variables

* `VAULT_SIGNING_KEY`: The matching secret key used to decrypt and verify the inbound token signature.
* `SOVEREIGN_CONTEXT_STRING`: The cryptographic salt or seed injected into the Airlock class to execute unique topological transformations.

---

## Quickstart Deployment

To spin up either service container locally or within a staging environment, navigate to the respective directory and utilize standard Docker instructions:

### 1. Build the Container

```bash
docker build -t sovereign-generator ./generator

```

### 2. Run the Container

```bash
docker run -e PORT=8080 \
           -e UI_DOMAIN_URL="https://example.com" \
           -e VAULT_SIGNING_KEY="your-high-entropy-secret-key" \
           -e SENDER_EMAIL="auth@example.com" \
           -e SENDER_PASSWORD="your-secure-smtp-password" \
           -p 8080:8080 sovereign-generator

```

---

## License

This framework is licensed under the Apache License, Version 2.0 (the "License"). You may not use this repository except in compliance with the License. You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

---



Distributed under the Apache 2.0 License. See LICENSE for more information.
