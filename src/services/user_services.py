from fastapi import HTTPException, status
from models.user_models import *
from repository.user_repository import getusers, createUser, updateUser
from secure.process_image import image_verification, generate_name_unique
from secure.file_secure import allowed_file
from werkzeug.utils import secure_filename
from secure.hash_password import generate_password
import os
from dotenv import load_dotenv

load_dotenv()

def listUsers(q: str | None = None):
    users = getusers(q)

    if users == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return users

async def newUser(username: str, password: str, image, role: str):
    archivo = "usuario_defecto.png"
    if image != None:
        if not allowed_file(image.filename):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image not allowed.")
        
        filename = secure_filename(image.filename)
        archivo = generate_name_unique(filename)
        file = "profiles"

    password_hash = generate_password(password)

    change = createUser(username, password_hash, archivo, role)
        
    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    if image != None:
        if not await image_verification(image, filename, file):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image format not allowed.")
            
        os.rename(os.path.join(os.getenv("UPLOAD_FOLDER_USERS"), filename), os.path.join(os.getenv("UPLOAD_FOLDER_USERS"), archivo))
    
    return 

async def updateaUser(username: str | None, password: str | None, image, role: str | None, id_external: str):
    if image != None:
        if not allowed_file(image.filename):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image not allowed.")
        filename = secure_filename(image.filename)
        archivo = generate_name_unique(filename)
        file = "profiles"

    password_hash = None
    if password != None:
        password_hash = generate_password(password)

    change = updateUser(username, password_hash, archivo, role, id_external)
        
    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    if image != None:
        if not await image_verification(image, filename, file):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image format not allowed.")
                
        os.rename(os.path.join(os.getenv("UPLOAD_FOLDER_USERS"), filename), os.path.join(os.getenv("UPLOAD_FOLDER_USERS"), archivo))
    
    return 
    