from fastapi import FastAPI, HTTPException, status, Response, Cookie, Depends, UploadFile, Form, File
from models.login_models import LoginRequest, LoginResponse
from models.inventory_models import *
from models.bin_models import *
from models.orders_model import *
from models.user_models import *
from models.agent_models import *
from models.pagination_models import * 
from services.auth_services import auth
from services.movements_Services import *
from services.bin_services import *
from services.orders_services import *
from services.user_services import *
from services.agent_services import *
from services.historial_movements_services import *
from middleware.auth_middleware import auth_verificator
from middleware.access_middleware import level_verificator
from typing import Optional

app = FastAPI(title="WMS app", description="Mini WMS + AI assistant app web project.", summary="Mini WMS + AI assistant app web.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

@app.post("/api/v1/auth/login")
def login(payload: LoginRequest, response: Response) -> LoginResponse:
    if payload.username == "" or payload.username == "string" or payload.password == "" or payload.password == "string":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fill all the fields.")

    token = auth(payload.username, payload.password)
   
    response.set_cookie(key="access_token", value=token, max_age=(8 * 60 * 60), secure=False, httponly=True, samesite='lax')
    
    return {"message": "Login successful, Welcome!"}

@app.post("/api/v1/auth/logout")
def logout(response: Response) -> LoginResponse:
    response.delete_cookie(key="access_token", secure=False, httponly=True, samesite='lax')
    return {"message": "Logout successful, have a great day!"}

@app.get("/api/v1/stock", dependencies=[Depends(auth_verificator)])
def stockPerBinList(page: int, limit: int = 20, search_query: str | None = None, bin_code: str | None = None):

    stock, limit_page = getStockPerBin(page, limit, search_query, bin_code)
    
    return PaginatedStockPerBinResponse(total_pages=limit_page, page=page, limit=limit, data=stock)

@app.get("/api/v1/inventory/historial_movements", dependencies=[Depends(auth_verificator)])
def movementsHistorial(page: int, limit: int = 20, item_id: str | None = None, movement_type: str | None = None, movement_external_id: str | None = None) -> PaginatedStockMovementsResponse:

    historial, limit_page = getMovementsHistorial(page, limit, item_id, movement_type, movement_external_id)
    
    return PaginatedStockMovementsResponse(total_pages=limit_page, page=page, limit=limit, data=historial)

@app.get("/api/v1/inventory/movements", dependencies=[Depends(auth_verificator)])
def movementsAll() -> list[MovementsResponse]:

    movements = getmovements()
    
    return [MovementsResponse(id_external=row[0], movement=row[1]) for row in movements] 

@app.post("/api/v1/inventory/receive", dependencies=[Depends(auth_verificator)])
def recieve(payload: InventoryReceiveRequest, access_token: str | None = Cookie(default=None)) -> InventoryReceiveResponse:
    
    message = recieveItems(payload, access_token)

    return {"message": message, "movement": payload.movement}


@app.post("/api/v1/inventory/receive-new", dependencies=[Depends(auth_verificator)], status_code=201)
async def recieveNew(sku: str = Form(..., max_length=150, description="product sku"), name: str = Form(..., max_length=100, description="product name"), description: Optional[str] = Form(None, description="description"), image: UploadFile = File(None, description="product image"),
    bin_id: str = Form(..., max_length=100, description="ID bin/localition"),
    quantity: int = Form(..., gt=0, description="initial quantity"),
    movement: str = Form(..., min_length=1, max_length=100, description="ID movement"), access_token: str | None = Cookie(default=None)) -> InventoryReceiveResponse:
    
    message = await recieveItemsNew(sku, name, description, image, bin_id, quantity, movement, access_token)

    return {"message": message, "movement": movement}

@app.post("/api/v1/inventory/transfer", dependencies=[Depends(auth_verificator)])
def transfer(payload: InventoryExchangeRequest, access_token: str | None = Cookie(default=None)) -> InventoryReceiveResponse:
    
    message = exchangeItems(payload, access_token)

    return {"message": message, "movement": payload.movement}

@app.get("/api/v1/bins", dependencies=[Depends(auth_verificator)])
def getbin() -> list[ListBins]:
    
    bins = listBin()

    return [ListBins(id_external=bin[0], generated_code=bin[1]) for bin in bins]

@app.post("/api/v1/bins", dependencies=[Depends(auth_verificator)], status_code=201)
def newbin(payload: BinCreate) -> LoginResponse:
    
    message = createBin(payload)

    return {"message": message}

@app.patch("/api/v1/bins/{bin_id}", dependencies=[Depends(auth_verificator)], status_code=204)
def updatebin(bin_id: str, payload: BinUpdateSchema):
    
    pathBin(payload, bin_id)

    return 

@app.get("/api/v1/orders", dependencies=[Depends(auth_verificator)])
def ordersAll(page: int, limit: int = 20, status: str | None = None) -> PaginatedOrdersResponse:

    orders, total_pages = getOrdersPaginated(page, limit, status)
  
    return PaginatedOrdersResponse(total_pages=total_pages, page=page, limit=limit, data=orders)

@app.get("/api/v1/orders_historial", dependencies=[Depends(auth_verificator)])
def ordersHistorial(page: int, limit: int = 20, q: str | None = None) -> PaginatedOrderStatusHistoryResponse:

    orders, total_pages = getOrderHistorial(page, limit, q)

    return PaginatedOrderStatusHistoryResponse(total_pages=total_pages, page=page, limit=limit, data=orders)

@app.get("/api/v1/orders/{id_external}", dependencies=[Depends(auth_verificator)])
def orderOne(id_external: str):

    order, data_items = getOrder(id_external)
    
    return OrderDetailResponseSchema(id_external=order[0], username=order[1], status=order[2], created_at=order[3], items=data_items)

@app.post("/api/v1/orders/create", dependencies=[Depends(auth_verificator)], status_code=201)
def createOrder(payload: OrderCreateSchema, access_token: str | None = Cookie(default=None)) -> OrderResponseSchema:

    response = createNewOrder(payload, access_token)

    return response

@app.post("/api/v1/orders/{id_external}/pick", dependencies=[Depends(auth_verificator)])
def pickOrder(id_external: str, access_token: str | None = Cookie(default=None)) -> OrderResponsePick:

    response = pickaOrder(id_external, access_token)

    return response

@app.post("/api/v1/orders/{id_external}/ship", dependencies=[Depends(auth_verificator)])
def shipOrder(id_external: str, access_token: str | None = Cookie(default=None)) -> OrderResponseShip:

    response = shipaOrder(id_external, access_token)

    return response

@app.post("/api/v1/users", dependencies=[Depends(auth_verificator), Depends(level_verificator)], status_code=201)
async def create_user(username: str = Form(..., max_length=100, description="usernam"), password: str = Form(..., min_length=6, description="password"), image: UploadFile = File(None, description="Profile image"), role_id: str = Form(..., description="rol id")):

    await newUser(username, password, image, role_id)

    return

@app.get("/api/v1/users", dependencies=[Depends(auth_verificator), Depends(level_verificator)])
def list_users(q: str | None = None) -> list[UserResponseSchema]:

    users = listUsers(q)
    
    return [UserResponseSchema(id_external=row[0], username=row[2], image=row[1]) for row in users]

@app.patch("/api/v1/users/{user_id}", dependencies=[Depends(auth_verificator), Depends(level_verificator)], status_code=204)
async def update_user(user_id: str, username: str = Form(None, max_length=100, description="username"), password: str = Form(None, min_length=6, description="password"), image: UploadFile = File(None, description="Profile image"),role_id: str = Form(None, description="rol id")) -> None:

    await updateaUser(username, password, image, role_id, user_id)
    
    return None

@app.post("/api/v1/ai/query", dependencies=[Depends(auth_verificator)])
async def ai_query_with_langchain(payload: AIQueryRequest):
    try:
        response = await run_wms_ai_agent(payload.question)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return response