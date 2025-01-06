from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    phone_number: str = Field(..., min_length=10, max_length=15)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
