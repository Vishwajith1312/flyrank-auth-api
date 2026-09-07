import requests

BASE_URL = "http://localhost:8002"

# Step 1: Log in
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "sigmatommy1800+flyranktest@gmail.com",
    "password": "password123"
})
print("Login status:", login_response.status_code)
data = login_response.json()
token = data["access_token"]
print("Got token, length:", len(token))

# Step 2: Use that token immediately on the protected route
profile_response = requests.get(f"{BASE_URL}/protected/profile", headers={
    "Authorization": f"Bearer {token}"
})
print("Profile status:", profile_response.status_code)
print("Profile response:", profile_response.json())