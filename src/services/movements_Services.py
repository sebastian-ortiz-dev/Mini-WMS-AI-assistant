from fastapi import HTTPException, status
from models.inventory_models import InventoryReceiveRequest, InventoryExchangeRequest
from repository.movements_repository import recieveProduct, recieveProductNew, exchangeBetweenBins, getmovements
from secure.decode import data_jwt
from secure.process_image import image_verification, generate_name_unique
from secure.file_secure import allowed_file
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

def movementlist():
    movement = getmovements()

    if movement == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to get the data.")
    
    return movement

def recieveItems(data: InventoryReceiveRequest, cookie: str) -> str:
    payload = data_jwt(cookie)
    change = recieveProduct(data.movement, payload['sub'], data.sku, data.quantity, data.bin_id)
    
    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return "Item recieve sucefully"

async def recieveItemsNew(sku: str, name: str, description: str, image, bin: str, quantity: int, movement: str, cookie: str) -> str:
    if not allowed_file(image.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image not allowed.")
    filename = secure_filename(image.filename)
    archivo = generate_name_unique(filename)
    file = "products"
    
    payload = data_jwt(cookie)
    change = recieveProductNew(movement, payload["sub"], quantity, bin, sku, name, archivo, description)
    
    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    if not await image_verification(image, filename, file):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image format not allowed.")
        
    os.rename(os.path.join(os.getenv("UPLOAD_FOLDER"), filename), os.path.join(os.getenv("UPLOAD_FOLDER"), archivo))

    return "Item recieve sucefully"
    
def exchangeItems(data: InventoryExchangeRequest, cookie: str) -> str:
    payload = data_jwt(cookie)
    change = exchangeBetweenBins(data.movement, payload["sub"], data.sku, data.quantity, data.from_bin_id, data.to_bin_id)
    
    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return "Item exchange sucefully"