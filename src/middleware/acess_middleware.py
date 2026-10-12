from fastapi import Cookie, HTTPException, status
from secure.decode import data_jwt

def auth_verificator(access_token: str | None = Cookie(default=None)):
    data = data_jwt(access_token)
    if data['level_acces'] != "Administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You haven't the require access.")
    return
    