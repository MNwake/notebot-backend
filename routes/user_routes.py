from fastapi import APIRouter, HTTPException
from models import UserRegister, UserLogin
from services.auth_service import AuthService

router = APIRouter()

@router.post("/register")
async def register_user(user: UserRegister):
    try:
        return await AuthService.register_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during registration")

@router.post("/login")
async def login_user(user: UserLogin):
    try:
        return await AuthService.login_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during login")
