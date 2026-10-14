from fastapi import HTTPException, status
from repository.orders_repository import createOrder, pickOrder, shipOrder, getOrders, getOneOrder
from models.orders_model import OrderCreateSchema, OrderResponseSchema, OrderResponsePick, OrderResponseShip, OrderListItemSchema, OrderItemDetailSchema
from secure.decode import data_jwt
import math

def getOrdersPaginated(page: int, limit: int = 20, status_filter: str | None = None):
    if page < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")
        
    offset = (page - 1) * limit

    orders, count = getOrders(limit, offset, status_filter)

    if orders == None or count == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")
    
    limit_pages = math.ceil(count[0] / limit)
    
    if page > limit_pages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page doesn't exist.")

    return [OrderListItemSchema(id_external=log[0], username=log[1], status=log[2], created_at=log[3]) for log in orders], limit_pages

def getOrder(id_external: str):

    order, items = getOneOrder(id_external)

    if order == None or items == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return order, [OrderItemDetailSchema(sku=log[0], name=log[1], bin_code=log[2], quantity_requested=log[3]) for log in items]

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