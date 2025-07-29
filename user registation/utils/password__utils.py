def hash_password(password: str) -> str:
    return password + "_hashed"

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed
