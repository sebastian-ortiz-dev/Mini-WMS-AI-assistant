from repository.login_repository import get_user
from secure.hash_password import verify
from fastapi import HTTPException, status
from secure.generate_JWT import create_jwt

def auth(username: str, password: str) -> str:
    user = get_user(username)

    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't exist.")

    if not verify(password, user[2]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User or password incorrect.")

    encode = create_jwt(user[0], user[1], user[3], user[4])

    return encode

    
        