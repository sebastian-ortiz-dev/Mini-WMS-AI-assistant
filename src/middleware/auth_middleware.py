from fastapi import Cookie, HTTPException, status
import jwt
from secure.decode import data_jwt

def auth_verificator(access_token: str | None = Cookie(default=None)):
    try:
        dato = data_jwt(access_token)
        return dato
    except jwt.ExpiredSignatureError as e:
        print(f"Token expirate: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expire session.")
    except jwt.InvalidTokenError as e:
        print(f"Token invalidate: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expire session.")
 