from pydantic import BaseModel, EmailStr
from typing import Optional
 
class RegisterRequest(BaseModel):
    username:str
    first_name:str
    last_name:str
    dob: str
    doj: str
    address: str
    comment: Optional[str]=" "
    active: bool
    password: str
 
 
class LoginRequest(BaseModel):
    username:str
    password: str
 
 
class TokenResopnse(BaseModel):
    access_token: str
    token_type: str = "bearer"
 
 
class PasswordChangeRequest(BaseModel):
    username:str
    old_password: str
    new_password:str
 
class ForgetPasswordRequest(BaseModel):
    username: int
    Mobilenumber: int
 
class ChangeContactRequest(BaseModel):
    new_email: Optional[EmailStr] = None
    new_phone: Optional[str] = None



    
