from repository.conexion_db import instance_conexion
from datetime import datetime

def getusers(q: str | None = None):
    sql = "SELECT id_external, image, username FROM public.users "
    parameters = None

    if q is not None and q != "" and q != "string":
        sql += " WHERE username ILIKE %s OR id_external ILIKE %s"
        parameters = (f"{q}%", f"{q}%")

    sql += " ORDER BY id ASC"
    
    pool, cursor = instance_conexion.init_conexion()
    if parameters == None:
        users = instance_conexion.all(cursor, sql)
    else:
        users = instance_conexion.all_parameters(cursor, sql, parameters)
    instance_conexion.close_conexion(cursor, pool)
    
    if users == None:
        return None
    
    return users

def createUser(username: str, password_hash: str, image: str, role: str):
    sql = "SELECT id FROM public.user_roles WHERE id_external=%s"
    parameters = (role,)

    pool, cursor = instance_conexion.init_conexion()
    role_id = instance_conexion.one(cursor, sql, parameters)

    if role_id == None:
        instance_conexion.close_conexion(cursor, pool)
        return None
    
    sql = "INSERT INTO public.users(id_external, username, password_hash, image, role_id, created_at) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s)"
    parameters = (username, password_hash, image, role_id[0], datetime.now())
    instance_conexion.register(cursor, sql, parameters)
    save = instance_conexion.execute_change(pool)
    instance_conexion.close_conexion(cursor, pool)

    if save == None:
        return None

    return True

def updateUser(username: str | None, password_hash: str | None , image: str | None , role: str | None, id_external: str):
    pool, cursor = instance_conexion.init_conexion()
    role_id = None
    if role != None:
        sql = "SELECT id FROM public.user_roles WHERE id_external=%s"
        parameters = (role,)
        role_id = instance_conexion.one(cursor, sql, parameters)
        if role_id == None:
            instance_conexion.close_conexion(cursor, pool)
            return None

    sql = "UPDATE public.users SET "
    parameters = ()
    fields = []

    if username is not None and username != "" and username != "string":
        fields.append("username = %s")
        parameters += (username,)

    if password_hash is not None and password_hash != "" and password_hash != "string":
        fields.append("password_hash = %s")
        parameters += (password_hash,)

    if image is not None and image != "" and image != "string":
        fields.append("image = %s")
        parameters += (image,)

    if role_id is not None and role_id != "" and role_id != "string":
        fields.append("role_id = %s")
        parameters += (role_id,)

    if not fields:
        return None, ()

    sql += ", ".join(fields)
    sql += " WHERE id_external = %s;"
    parameters += (id_external,)
    instance_conexion.register(cursor, sql, parameters)
    save = instance_conexion.execute_change(pool)
    instance_conexion.close_conexion(cursor, pool)

    if save == None:
        return None

    return True
