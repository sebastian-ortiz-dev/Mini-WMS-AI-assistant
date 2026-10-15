from fastapi.testclient import TestClient
import os
import pytest
import shutil
from dotenv import load_dotenv
from testcontainers.postgres import PostgresContainer
from src.repository.conexion_db import instance_conexion
from src.main import app

load_dotenv()

postgres = PostgresContainer("postgres:17-alpine", username="postgres", password="123", dbname="wms_db")
base = os.path.dirname(os.path.abspath(__file__))
sql_ruta = os.path.join(base, "../db", "wms_db.sql")
seeds_route = os.path.join(base, "../db", "seed.sql")
folder_ruta = os.path.join(base, "..", "base_test_images")


@pytest.fixture(scope="session", autouse=True)
def test_folder():
    sub_folder_product = os.path.join(folder_ruta, "products")
    sub_folder_perfil = os.path.join(folder_ruta, "profile")
    # Create the folder images test
    os.mkdir(folder_ruta)
    os.mkdir(sub_folder_product)
    os.mkdir(sub_folder_perfil)

    yield

    # delete the folder
    shutil.rmtree(folder_ruta)

@pytest.fixture(scope="session", autouse=True)
def postgres_db_test():
    postgres.start() 

    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USER"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname

    with open(sql_ruta, "r") as file:
        sql = file.read()

    pool, cursor = instance_conexion.init_conexion()
    cursor.execute(sql)
    instance_conexion.execute_change(pool)

    with open(seeds_route, "r") as file:
        seed = file.read()

    cursor.execute(seed)
    instance_conexion.execute_change(pool)
    instance_conexion.close_conexion(cursor, pool)

    yield

    postgres.stop()

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def create_jwt(client):
    credentials = ["admin", "123"]

    client.post("/api/v1/auth/login", json={
        "username": credentials[0],
        "password": credentials[1],
    })

    return client

@pytest.fixture()
def create_jwt_worker(client):
    credentials = ["worker", "123"]

    client.post("/api/v1/auth/login", json={
        "username": credentials[0],
        "password": credentials[1],
    })

    return client
