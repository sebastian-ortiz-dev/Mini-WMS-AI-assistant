from dotenv import load_dotenv
import jwt
import os

load_dotenv()

def data_jwt(encode):
    decode = jwt.decode(encode, key=os.getenv("KEY"), algorithms="HS256")
    return decode