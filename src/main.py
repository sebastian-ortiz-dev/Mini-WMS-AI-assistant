from fastapi import FastAPI, HTTPException, status, Response, Cookie, Depends, UploadFile, Form, File
from models.login_models import LoginRequest, LoginResponse
from models.inventory_models import *
from models.bin_models import *
from services.auth_services import auth
from services.movements_Services import *
from services.bin_services import *
from middleware.auth_middleware import auth_verificator
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
def logout(response: Response, access_token: str | None = Cookie(default=None)) -> LoginResponse:
    response.delete_cookie(key="access_token", secure=False, httponly=True, samesite='lax')
    return {"message": "Logout successful, have a great day!"}

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
def newbin() -> list[ListBins]:
    
    bins = listBin()

    return [ListBins(id_external=bin[0], generated_code=bin[1]) for bin in bins]

@app.post("/api/v1/bins", dependencies=[Depends(auth_verificator)], status_code=201)
def newbin(payload: BinCreate) -> LoginResponse:
    
    message = createBin(payload)

    return {"message": message}