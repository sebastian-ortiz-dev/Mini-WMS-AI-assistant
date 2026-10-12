from repository.conexion_db import instance_conexion

def newBin(aisle: int, bay: str, tier: int, position: str, generated_code: str):
    sql = "INSERT INTO public.bins(id_external, aisle, bay, tier, position, generated_code) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s)"
    parameters = (aisle, bay, tier, position, generated_code)

    pool, cursor = instance_conexion.init_conexion()
    instance_conexion.register(cursor, sql, parameters)
    save = instance_conexion.execute_change(pool)
    instance_conexion.close_conexion(cursor, pool)

    if not save:
        return None

    return save

def GetBins():
    sql = "SELECT id_external, generated_code FROM public.bins ORDER BY id ASC"

    pool, cursor = instance_conexion.init_conexion()
    bins = instance_conexion.all(cursor, sql)
    instance_conexion.close_conexion(cursor, pool)

    if bins == None:
        return None

    return bins