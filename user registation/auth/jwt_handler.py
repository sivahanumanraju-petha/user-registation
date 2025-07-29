from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
 
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
 
blacklist = set()
 
def create_access_token(username: str):
    data = {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
 
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
 
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in blacklist:
        raise HTTPException(status_code=401, detail="Token revoked")
    return decode_token(token)
 
def deactivate_token(token: str):
    blacklist.add(token)