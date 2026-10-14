from repository.pagination_repository import *
from models.pagination_models import *
from fastapi import HTTPException, status
import math

def getMovementsHistorial(page: int, limit: int = 20, item_id: str | None = None, movement_type: str | None = None, movement_external_id: str | None = None):
    if page < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")
    
    offset = (page - 1) * limit

    historial, count = get_stock_movements_paginated(limit, offset, movement_type, item_id, movement_external_id)

    if historial == None or count == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    limit_pages = math.ceil(count[0] / limit)

    if page > limit_pages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")
    
    return [StockMovementItemResponse(id_external=log[0], username=log[1], movement=log[2], quantity=log[3], item_name=log[4], sku=log[5], from_bin_code=log[6], to_bin_code=log[7], created_at=log[8]) for log in historial], limit_pages

def getStockPerBin(page: int, limit: int, search_query: str | None = None, bin_code: str | None = None):
    if page < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")
    
    offset = (page - 1) * limit

    stocks, count = get_stock_per_bin_paginated(limit, offset, search_query, bin_code)

    if stocks == None or count == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    limit_pages = math.ceil(count[0] / limit)

    if page > limit_pages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")
    
    return  [StockPerBinItemResponse(sku=log[0], name=log[1], image=log[2], bin_code=log[3], quantity_available=log[4], quantity_reserved=log[5]) for log in stocks], limit_pages