import os
from psycopg2 import pool
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

class Conexion:
    connection_db = None
    
    def init_conexion(self):
        try:
            if self.connection_db == None:
                self.connection_db = pool.ThreadedConnectionPool(
                        1, 15, 
                        dbname=os.getenv('DB_NAME'), 
                        user=os.getenv('DB_USER'), 
                        password=os.getenv('DB_PASSWORD'), 
                        host=os.getenv('DB_HOST'), 
                        port=os.getenv('DB_PORT')
                    )
            
            pool_db = self.connection_db.getconn()
            cursor = pool_db.cursor()
            return pool_db, cursor
        except Exception as e:
            print("Has occurred an error to try connect to DB: ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Database connection error"
            )

    def all(self, cursor, sql):
        cursor.execute(sql)
        return cursor.fetchall()
    
    def all_parameters(self, cursor, sql, parameters):
        cursor.execute(sql, parameters)
        return cursor.fetchall()

    def one(self, cursor, sql, parameters):
        cursor.execute(sql, parameters)
        return cursor.fetchone()        

    def register(self, cursor, sql, parameters):
        try:
            cursor.execute(sql, parameters)
            return True
        except Exception as e:
            print("has ocurred a error: ", e)
            return False
    
    def execute_change(self, pool_db):
        try:
            pool_db.commit()
            return True
        except Exception as e:
            self.revert_changes(pool_db)
            print("Has occurred an error to try execute changes in db: ", e)
            return False
        
    def revert_changes(self, pool_db):
        pool_db.rollback()

    def close_conexion(self, cursor, pool_db):
        cursor.close()
        self.connection_db.putconn(pool_db)

instance_conexion = Conexion()