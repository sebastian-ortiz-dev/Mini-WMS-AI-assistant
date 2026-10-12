from dotenv import load_dotenv
import jwt
import time
import math
import os

load_dotenv()
#(8 * 60 * 60)
def create_jwt(sub, name, image, level_acces):
    iat = math.floor(time.time())
    exp = iat + (15 * 60)
    encode = jwt.encode({ "iss": "wms", "sub": f"{sub}", "username": name, "image": image, "level_acces": level_acces, "iat": iat, "exp": exp }, key=os.getenv("KEY"), algorithm="HS256")
    return encode