import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import uuid

keys = []  # Key storage

def generate_key_pair():
    """Generate an RSA key pair and store it with metadata."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    kid = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(minutes=10)  # Keys expire in 10 minutes

    keys.append({
        "kid": kid,
        "private_key": private_pem.decode(),
        "public_key": public_pem.decode(),
        "expiry": expiry,
        "expired": False
    })
    return keys

def get_active_keys(keys):
    """Return active (non-expired) keys in JWKS format."""
    active_keys = []
    for key in keys:
        if key["expiry"] > datetime.utcnow():
            key["expired"] = False
            active_keys.append({
                "kty": "RSA",
                "use": "sig",
                "kid": key["kid"],
                "alg": "RS256",
                "n": jwt.utils.base64url_encode(key["public_key"].encode()).decode(),
                "e": "AQAB"
            })
        else:
            key["expired"] = True
    return active_keys

def get_key_by_kid(kid):
    """Retrieve a specific key by Key ID."""
    for key in keys:
        if key["kid"] == kid:
            return key
    return None
