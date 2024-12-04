import requests

BASE_URL = "http://localhost:8080"

# Test the /jwks endpoint
print("Testing JWKS Endpoint")
response = requests.get(f"{BASE_URL}/jwks")
print("JWKS Response:", response.json())

# Test the /auth endpoint for an unexpired JWT
print("Testing Auth Endpoint (Unexpired JWT)")
response = requests.post(f"{BASE_URL}/auth")
print("Auth Response:", response.json())

# Test the /auth endpoint for an expired JWT
print("Testing Auth Endpoint (Expired JWT)")
response = requests.post(f"{BASE_URL}/auth?expired=true")
print("Auth Response (Expired):", response.json())
