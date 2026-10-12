from passlib.hash import pbkdf2_sha256

def verify(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)

def generate_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)