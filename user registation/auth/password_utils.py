from passlib.context import CryptContext
import re
from datetime import datetime, timedelta
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
def get_password_hash(password):
    return pwd_context.hash(password)
 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
 
def is_password_strong(password):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,20}$", password))
 
def is_password_expired(password_updated_at: str) -> bool:
    updated = datetime.fromisoformat(password_updated_at)
    return datetime.now() - updated > timedelta(days=30)