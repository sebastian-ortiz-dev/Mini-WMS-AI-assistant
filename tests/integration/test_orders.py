import pytest

def test_create_order_success(create_jwt):
    """
    Test Scenario: Successful Order Creation (Happy Path)
    - Input: Valid item SKU, existing bin external ID, and a positive quantity.
    - Expected Behavior: Returns status code 201 Created.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED",  
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35", 
                "quantity": 5
            }
        ]
    }
    response = create_jwt.post("/api/v1/orders/create", json=payload)
    assert response.status_code == 201

def test_create_order_item_or_bin_not_exists(create_jwt):
    """
    Test Scenario: Business Validation - Non-existent Item or Bin
    - Input: An invalid item SKU ("SKU-FALSE") combined with a valid bin ID.
    - Expected Behavior: Returns status code 400 Bad Request with a specific error detail 
      indicating that the item or bin does not exist.
    """
    payload = {
        "items": [
            {
                "item_sku": "SKU-FALSE",
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35",
                "quantity": 1
            }
        ]
    }
    
    response = create_jwt.post("/api/v1/orders/create", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "The item or bin don't exist."


def test_create_order_invalid_quantity(create_jwt):
    """
    Test Scenario: Pydantic Validation - Invalid Quantity
    - Input: Quantity set to 0 (violating the model's positive constraint).
    - Expected Behavior: Returns status code 422 Unprocessable Entity due to schema validation failure.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED",
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35",
                "quantity": 0  
            }
        ]
    }
    
    response = create_jwt.post("/api/v1/orders/create", json=payload)
    assert response.status_code == 422


def test_create_order_missing_fields(create_jwt):
    """
    Test Scenario: Pydantic Validation - Missing Required Payload Fields
    - Input: An order payload missing mandatory attributes like bin ID and quantity.
    - Expected Behavior: Returns status code 422 Unprocessable Entity.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED"
            }
        ]
    }
    
    response = create_jwt.post("/api/v1/orders/create", json=payload)
    assert response.status_code == 422


def test_create_order_unauthorized(client):
    """
    Test Scenario: Security & Authentication - Unauthorized Access
    - Input: POST request to create an order without providing an authentication token/cookie.
    - Expected Behavior: Returns status code 401 Unauthorized via the unauthenticated test client.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED",
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35",
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/api/v1/orders/create", json=payload)
    assert response.status_code == 401

def test_pick_order_success(create_jwt):
    """
    Test Scenario: Successful Order Picking (Happy Path)
    - Input: Dynamically creates an order first, extracts its external ID, and calls the pick endpoint.
    - Expected Behavior: Returns status code 200 OK indicating the picking process succeeded.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED",
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35",
                "quantity": 1
            }
        ]
    }
    create_res = create_jwt.post("/api/v1/orders/create", json=payload)
    assert create_res.status_code == 201
    
    order_data = create_res.json()
    order_id = order_data.get("id_external") or order_data.get("id")

    pick_res = create_jwt.post(f"/api/v1/orders/{order_id}/pick")
    assert pick_res.status_code == 200 


def test_pick_order_not_found(create_jwt):
    """
    Test Scenario: Business Validation - Pick Non-existent Order ID
    - Input: Attempts to pick using a hardcoded dummy UUID that does not exist in the database.
    - Expected Behavior: Returns a client error status code (400 or 404).
    """
    fake_id = "00000000-0000-0000-0000-000000000099"
    response = create_jwt.post(f"/api/v1/orders/{fake_id}/pick")
    assert response.status_code in [400, 404]


def test_ship_order_success(create_jwt):
    """
    Test Scenario: Full Order Lifecycle Flow - Successful Shipping (Happy Path)
    - Input: Creates an order, performs the required picking step, and then calls the ship endpoint.
    - Expected Behavior: Returns status code 200 OK confirming the shipment.
    """
    payload = {
        "items": [
            {
                "item_sku": "LAM-ESC-NG-LED",
                "bin_id_external": "2a7d056a-2139-4141-befc-db84f79e8d35",
                "quantity": 1
            }
        ]
    }
    create_res = create_jwt.post("/api/v1/orders/create", json=payload)
    order_data = create_res.json()
    order_id = order_data.get("id_external") or order_data.get("id")

    # Order must be picked before shipping according to business logic flow
    create_jwt.post(f"/api/v1/orders/{order_id}/pick")

    ship_res = create_jwt.post(f"/api/v1/orders/{order_id}/ship")
    assert ship_res.status_code == 200