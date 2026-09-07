import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client
from fastapi import HTTPException, status, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("Server running and connected to Supabase")

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}
from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthRequest):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.post("/auth/login")
def login(credentials: AuthRequest):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")
def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer ") or len(auth_header.split(" ")) != 2:
        raise HTTPException(status_code=401, detail="Access token required")

    token = auth_header.split(" ")[1]

    try:
        user_response = supabase.auth.get_user(token)
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/protected/profile")
def protected_profile(auth_data: dict = Depends(verify_token)):
    user = auth_data["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }