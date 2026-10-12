from repository.conexion_db import instance_conexion

def get_user(username: str):
    sql = "SELECT u.id_external, u.username, u.password_hash, u.image, r.role_name FROM public.users u INNER JOIN public.user_roles r ON u.role_id=r.id WHERE u.username=%s"
    parameters = (username,)

    pool, cursor = instance_conexion.init_conexion()
    user = instance_conexion.one(cursor, sql, parameters)

    instance_conexion.close_conexion(cursor, pool)

    if user == None:
        return None

    return user