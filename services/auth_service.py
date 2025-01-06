# auth_service.py

from fastapi import HTTPException, status

from models import UserRegister, UserLogin
from database import User
from utils import pwd_context




class AuthService:
    @staticmethod
    async def register_user(user: UserRegister):
        try:
            # Check if the user already exists
            if User.objects(email=user.email).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Hash the password
            hashed_password = pwd_context.hash(user.password)

            # Create and save a new User document in MongoDB
            new_user = User(
                email=user.email,
                hashed_password=hashed_password,
                full_name=user.full_name,
                phone_number=user.phone_number
            )
            new_user.save()

            return {"msg": "User registered successfully", "user_id": str(new_user.id)}

        except HTTPException as http_exc:
            # Directly raise the HTTPException if already defined
            raise http_exc

        except Exception as e:
            # Log the error and provide a generic error message to the client
            print(f"Error during user registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user due to an unexpected error. Please try again later."
            )

    @staticmethod
    async def login_user(user: UserLogin):
        try:
            # Find the user by email
            existing_user = User.objects(email=user.email).first()
            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid credentials: user not found"
                )

            # Verify password
            if not pwd_context.verify(user.password, existing_user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid credentials: incorrect password"
                )

            return {"msg": "Login successful", "user_id": str(existing_user.id)}

        except HTTPException as http_exc:
            # Directly raise the HTTPException if already defined
            raise http_exc

        except Exception as e:
            # Log the error and provide a generic error message to the client
            print(f"Error during user login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to login due to an unexpected error. Please try again later."
            )
