import bcrypt


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty.")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password:
        raise ValueError("Password cannot be empty.")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
