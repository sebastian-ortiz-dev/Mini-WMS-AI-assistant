from repository.conexion_db import instance_conexion
from fastapi import HTTPException, status
from datetime import datetime

def getmovements():
    sql = "SELECT id_external, movement FROM public.movements ORDER BY id ASC "
    pool, cursor = instance_conexion.init_conexion()
    movements = instance_conexion.all(cursor, sql)
    instance_conexion.close_conexion(cursor, pool)

    if movements == None:
        return None
    
    return movements

def recieveProduct(movement: str, user: str, item_sku: str, quantity: int, bin: str):
    sql = "SELECT m.id FROM movements m WHERE id_external=%s"
    parameters = (movement,)
    pool, cursor = instance_conexion.init_conexion()
    movementeGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)
    userGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT i.id FROM public.items i WHERE i.sku=%s"
    parameters = (item_sku,)
    itemGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT b.id FROM public.bins b WHERE b.id_external=%s"
    parameters = (bin,)
    binGet = instance_conexion.one(cursor, sql, parameters)

    if movementeGet == None or userGet == None or itemGet == None or binGet == None:
        instance_conexion.close_conexion(cursor, pool)
        return None

    sql = "INSERT INTO public.stock_movements(id_external, user_id, action_type, created_at) VALUES (gen_random_uuid(), %s, %s, %s) RETURNING id"
    parameters = (userGet[0], movementeGet[0], datetime.now())
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None
    
    movementeId = cursor.fetchone()

    sql = "INSERT INTO public.stock_movement_items(movement_id, item_id, quantity, to_bin_id) VALUES (%s, %s, %s, %s)"
    parameters = (movementeId[0], itemGet[0], quantity, binGet[0])
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None

    sql = "INSERT INTO public.stock_per_bin(item_id, bin_id, quantity_available, quantity_reserved) VALUES (%s, %s, %s, 0) ON CONFLICT (item_id, bin_id) DO UPDATE SET quantity_available = stock_per_bin.quantity_available + %s"
    parameters = (itemGet, binGet, quantity, quantity)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None

    save = instance_conexion.execute_change(pool)

    instance_conexion.close_conexion(cursor, pool)

    if not save:
        return None

    return save

def recieveProductNew(movement: str, user: str, quantity: int, bin: str, item_sku: str, name: str, image: str, description: str):
    sql = "SELECT m.id FROM movements m WHERE id_external=%s"
    parameters = (movement,)
    pool, cursor = instance_conexion.init_conexion()
    movementeGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)
    userGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT b.id FROM public.bins b WHERE b.id_external=%s"
    parameters = (bin,)
    binGet = instance_conexion.one(cursor, sql, parameters)

    if movementeGet == None or userGet == None or binGet == None:
        instance_conexion.close_conexion(cursor, pool)
        return None
    
    sql = "INSERT INTO public.items(id_external, sku, name, image, description, created_at) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s) RETURNING id"
    parameters = (item_sku, name, image, description, datetime.now())
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None
    
    itemGet = cursor.fetchone()
    
    sql = "INSERT INTO public.stock_movements(id_external, user_id, action_type, created_at) VALUES (gen_random_uuid(), %s, %s, %s) RETURNING id"
    parameters = (userGet[0], movementeGet[0], datetime.now())
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None
    movementeId = cursor.fetchone()
    
    sql = "INSERT INTO public.stock_movement_items(movement_id, item_id, quantity, to_bin_id) VALUES (%s, %s, %s, %s)"
    parameters = (movementeId[0], itemGet[0], quantity, binGet[0])
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None

    sql = "INSERT INTO public.stock_per_bin(item_id, bin_id, quantity_available, quantity_reserved) VALUES (%s, %s, %s, 0)"
    parameters = (itemGet, binGet, quantity)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None

    save = instance_conexion.execute_change(pool)

    instance_conexion.close_conexion(cursor, pool)

    if not save:
        return None

    return save

def exchangeBetweenBins(movement: str, user: str, item_sku: str, quantity: int, binI: str, binO: str):
    sql = "SELECT m.id FROM movements m WHERE id_external=%s"
    parameters = (movement,)
    pool, cursor = instance_conexion.init_conexion()
    movementeGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)   
    userGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT i.id FROM public.items i WHERE i.sku=%s"
    parameters = (item_sku,)   
    itemGet = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT b.id FROM public.bins b WHERE b.id_external=%s"
    parameters = (binI,)
    binGetI = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT b.id FROM public.bins b WHERE b.id_external=%s"
    parameters = (binO,)
    binGetO = instance_conexion.one(cursor, sql, parameters)
    
    if movementeGet == None or userGet == None or itemGet == None or binGetI == None or binGetO == None:
        instance_conexion.close_conexion(cursor, pool)
        return None

    sql = "SELECT id FROM public.stock_per_bin s WHERE s.item_id = %s AND s.bin_id = %s AND s.quantity_available - s.quantity_reserved >= %s FOR UPDATE"
    parameters = (itemGet[0], binGetI[0], quantity)
    enough = instance_conexion.one(cursor, sql, parameters)
    if enough == None:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The item doesn't have the enough quantity.")

    sql = "INSERT INTO public.stock_movements(id_external, user_id, action_type, created_at) VALUES (gen_random_uuid(), %s, %s, %s) RETURNING id"
    parameters = (userGet[0], movementeGet[0], datetime.now())
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None
    movementeId = cursor.fetchone()

    sql = "INSERT INTO public.stock_movement_items(movement_id, item_id, quantity,from_bin_id, to_bin_id) VALUES (%s, %s, %s, %s, %s)"
    parameters = (movementeId[0], itemGet[0], quantity, binGetI[0], binGetO[0])
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        return None
   
    sql = "UPDATE public.stock_per_bin SET quantity_available= stock_per_bin.quantity_available - %s WHERE item_id = %s AND bin_id = %s"
    parameters = (quantity, itemGet[0], binGetI[0])
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The item doesn't have the enough quantity.")

    sql = "INSERT INTO public.stock_per_bin(item_id, bin_id, quantity_available, quantity_reserved) VALUES (%s, %s, %s, 0) ON CONFLICT (item_id, bin_id) DO UPDATE SET quantity_available = stock_per_bin.quantity_available + %s"
    parameters = (itemGet, binGetO[0], quantity, quantity)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None

    save = instance_conexion.execute_change(pool)

    instance_conexion.close_conexion(cursor, pool)

    if not save:
        return None

    return save