from fastapi import HTTPException, status
from repository.orders_repository import createOrder, pickOrder, shipOrder
from models.orders_model import OrderCreateSchema, OrderResponseSchema, OrderResponsePick, OrderResponseShip
from secure.decode import data_jwt

def createNewOrder(data: OrderCreateSchema, cookie: str) -> OrderResponseSchema:
    payload = data_jwt(cookie)
    save, order, date = createOrder(payload['sub'], data)

    if save == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    response = OrderResponseSchema(id_external=order, created_at=date)
    
    return response

def pickaOrder(data: str, cookie: str) -> OrderResponsePick:
    payload = data_jwt(cookie)
    save, order, date = pickOrder(payload["sub"], data)

    if save == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    response = OrderResponsePick(id_external=order, picked_at=date)
    
    return response

def shipaOrder(data: str, cookie: str) -> OrderResponseShip:
    payload = data_jwt(cookie)
    save, order, date = shipOrder(payload["sub"], data)

    if save == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    response = OrderResponseShip(id_external=order, shipped_at=date)
    
    return response