from PIL import Image
import os
import io
import uuid
from dotenv import load_dotenv

load_dotenv()

async def image_verification(picture, filename, file):
    binary = await picture.read()
    await picture.seek(0)
    im = Image.open(io.BytesIO(binary))
    if im.format.lower() not in os.getenv('ALLOWED_EXTENSIONS'):
        return False
    im.seek(0)      
    if file == "products":
        route = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
    else:
        route = os.path.join(os.getenv("UPLOAD_FOLDER_USERS"), filename)
    im.save(route)
    im.close()
    return True

def generate_name_unique(picture):
    extension = os.path.splitext(picture)[1]
    new_name = f'{uuid.uuid4()}{extension}'
    return new_name