from flask import Flask, jsonify, request
import jwt
import datetime
from keys import generate_key_pair, get_active_keys, get_key_by_kid

app = Flask(__name__)
keys = generate_key_pair()  # Initialize key storage with a single RSA key pair

@app.route('/jwks', methods=['GET'])
def jwks():
    """Serve active keys in JWKS format."""
    active_keys = get_active_keys(keys)
    jwks = {"keys": active_keys}
    return jsonify(jwks), 200

@app.route('/auth', methods=['POST'])
def auth():
    """Issue JWTs."""
    expired = request.args.get('expired', default=False, type=bool)
    
    # Check for active or expired keys
    key = next((k for k in keys if (k["expired"] == expired)), None)
    
    if not key:
        return jsonify({"error": "No matching key found"}), 404

    # Create payload with expiration logic
    payload = {
        "sub": "user123",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30 if not expired else -30),
        "iat": datetime.datetime.utcnow()
    }
    
    # Encode JWT
    token = jwt.encode(payload, key["private_key"], algorithm="RS256", headers={"kid": key["kid"]})
    
    return jsonify({"token": token}), 200

if __name__ == '__main__':
    app.run(port=8080)
  