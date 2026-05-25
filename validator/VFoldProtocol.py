import base64

class VFoldProtocol:
    """
    V-Fold Transpositional Lattice Protocol.
    Executes a deterministic, space-isolated transformation of raw identity profiles
    using a sovereign context seed.
    """
    def __init__(self, sovereign_string: str):
        if not sovereign_string:
            raise ValueError("Sovereign context boundary cannot be empty.")
        self.sovereign_string = sovereign_string.encode('utf-8')

    def fold(self, email: str) -> str:
        if not email:
            raise ValueError("Identity payload target cannot be empty.")
            
        email_bytes = email.encode('utf-8')
        folded_bytes = bytearray(len(email_bytes))

        for i in range(len(email_bytes)):
            email_char_val = email_bytes[i]
            sovereign_char_val = self.sovereign_string[i % len(self.sovereign_string)]

            # Deterministic positional transposition lattice
            transformed_val = (email_char_val ^ sovereign_char_val ^ (i % 256))
            folded_bytes[i] = transformed_val

        # Map to an URL-safe, compact topological representation
        return base64.urlsafe_b64encode(folded_bytes).decode('utf-8').rstrip('=')

    def unfold(self, folded_email: str) -> str:
        if not folded_email:
            raise ValueError("Folded identity handle target cannot be empty.")

        # Re-establish standard structural padding for execution alignment
        missing_padding = len(folded_email) % 4
        if missing_padding:
            folded_email += '=' * (4 - missing_padding)

        decoded_bytes = base64.urlsafe_b64decode(folded_email.encode('utf-8'))
        unfolded_bytes = bytearray(len(decoded_bytes))

        for i in range(len(decoded_bytes)):
            transformed_val = decoded_bytes[i]
            sovereign_char_val = self.sovereign_string[i % len(self.sovereign_string)]
            
            # Reverse the positional transposition lattice
            original_val = (transformed_val ^ sovereign_char_val ^ (i % 256))
            unfolded_bytes[i] = original_val

        return unfolded_bytes.decode('utf-8')
