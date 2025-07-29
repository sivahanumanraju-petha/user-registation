from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import(
RegisterRequest,
ChangeContactRequest,
PasswordChangeRequest,
ForgetPasswordRequest
)
from auth.password_utils import get_password_hash, verify_password, is_password_strong, is_password_expired
from auth.jwt_handler import create_access_token, decode_token, get_current_user
from database.json_db import get_user_by_username, save_user, update_user_password, update_user_contact, store_password_history, count_recent_password_resets, deactivate_token
from utils.logger import log_action
from datetime import datetime, timedelta
 
router = APIRouter()
 
@router.post("/register")
def register(user: RegisterRequest):
    log_action(f"Incoming user: {user}")
    existing = get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    if not is_password_strong(user.password):
        raise HTTPException(status_code=400, detail="Password does not meet security requirements")
    hashed = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed
    user_dict["password_updated_at"] = datetime.now().isoformat()
    save_user(user_dict)
    store_password_history(user.username, hashed)
    return {"msg": "User registered successfully"}
 
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form.username)
    if not user or not verify_password(form.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if is_password_expired(user['password_updated_at']):
        raise HTTPException(status_code=403, detail="Password expired, change required")
    token = create_access_token(user['username'])
    return {"access_token": token, "token_type": "bearer"}
 
@router.post("/change-contact")
def change_contact(data: ChangeContactRequest, username: str = Depends(get_current_user)):
    update_user_contact(username, data.new_contact)
    return {"msg": "Contact updated"}
 
@router.post("/change-password")
def change_password(data: PasswordChangeRequest, username: str = Depends(get_current_user)):
    user = get_user_by_username(username)
    if not verify_password(data.old_password, user['password']):
        raise HTTPException(status_code=401, detail="Old password incorrect")
    if not is_password_strong(data.new_password):
        raise HTTPException(status_code=400, detail="New password does not meet policy")
    hashed = get_password_hash(data.new_password)
    update_user_password(username, hashed)
    store_password_history(username, hashed)
    return {"msg": "Password changed"}
 
@router.post("/forget-password")
def forget_password(data: ForgetPasswordRequest):
    count = count_recent_password_resets(data.username)
    if count >= 3:
        raise HTTPException(status_code=429, detail="Max attempts reached. Try later.")
    # Token logic omitted for brevity
    return {"msg": "Reset email sent"}
 
@router.post("/logout")
def logout(token: str = Depends(get_current_user)):
    deactivate_token(token)
    return {"msg": "Logged out"}