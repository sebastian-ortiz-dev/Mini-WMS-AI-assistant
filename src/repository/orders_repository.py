from repository.conexion_db import instance_conexion
from models.orders_model import OrderCreateSchema
from fastapi import HTTPException, status
from datetime import datetime

def getOrders(limit: int, offset: int, status_filter: str | None = None):
    sql = "SELECT  o.id_external, u.username, os.status AS order_status, o.created_at FROM public.orders o INNER JOIN public.users u ON o.created_by = u.id INNER JOIN public.order_status os ON o.status = os.id "
    sql_count = "SELECT  COUNT(*) FROM public.orders o INNER JOIN public.users u ON o.created_by = u.id INNER JOIN public.order_status os ON o.status = os.id "

    filters = []
    parameters = ()
    filters_count = []
    parameters_count = ()
    
    pool, cursor = instance_conexion.init_conexion()

    if status_filter is not None and status_filter != "" and status_filter != "string":
        filters.append("os.status ILIKE %s")
        filters_count.append("os.status ILIKE %s")
        parameters += (f"%{status_filter}%",)
        parameters_count += (f"%{status_filter}%",)

    if filters:
        sql += " WHERE " + " AND ".join(filters)
        sql_count += " WHERE " + " AND ".join(filters_count)

    sql += " ORDER BY o.id DESC LIMIT %s OFFSET %s;"
    parameters += (limit, offset)

    orders = instance_conexion.all_parameters(cursor, sql, parameters)
    count = instance_conexion.one(cursor, sql_count, parameters_count)
    
    instance_conexion.close_conexion(cursor, pool)

    return orders, count[0]

def getOneOrder(id_external: str):
    sql = "SELECT o.id_external, u.username, os.status AS order_status, o.created_at FROM public.orders o INNER JOIN public.users u ON o.created_by = u.id INNER JOIN public.order_status os ON o.status = os.id WHERE o.id_external = %s"
    parameters = (id_external, )

    pool, cursor = instance_conexion.init_conexion()

    order = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT i.sku, i.name, b.generated_code AS bin_code, oi.quantity_requested FROM public.order_items oi INNER JOIN public.items i ON oi.item_id = i.id INNER JOIN public.bins b ON oi.bin_id = b.id INNER JOIN public.orders o ON oi.order_id = o.id WHERE o.id_external = %s"

    items = instance_conexion.all_parameters(cursor, sql, parameters)

    instance_conexion.close_conexion(cursor, pool)

    return order, items


def createOrder(user: str, items: OrderCreateSchema):
    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)
    pool, cursor = instance_conexion.init_conexion()
    userGet = instance_conexion.one(cursor, sql, parameters)
    date = datetime.now()

    itemList = []
    binList = []

    for row in items.items:
        sql = "SELECT i.id FROM public.items i WHERE i.sku=%s"
        parameters = (row.item_sku,)
        itemGet = instance_conexion.one(cursor, sql, parameters)
        
        sql = "SELECT b.id FROM public.bins b WHERE b.id_external=%s"
        parameters = (row.bin_id_external,)
        binGet = instance_conexion.one(cursor, sql, parameters)

        if itemGet == None or binGet == None:
            instance_conexion.close_conexion(cursor, pool)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The item or bin don't exist.")

        sql = "SELECT id FROM public.stock_per_bin s WHERE s.item_id = %s AND s.bin_id = %s AND s.quantity_available - s.quantity_reserved >= %s FOR UPDATE"
        parameters = (itemGet[0], binGet[0], row.quantity)
        enough = instance_conexion.one(cursor, sql, parameters)
        if enough == None:
            instance_conexion.close_conexion(cursor, pool)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The item doesn't have the enough quantity.")

        itemList.append(itemGet[0])
        binList.append(binGet[0])

    if userGet == None:
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    sql = "INSERT INTO public.orders(id_external, status, created_by, created_at) VALUES (gen_random_uuid(), 1, %s, %s) RETURNING id, id_external"
    parameters = (userGet[0], date)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None
    orderId = cursor.fetchone()

    for row in range(len(items.items)):
        sql = "INSERT INTO public.order_items(id_external, order_id, item_id, quantity_requested, bin_id) VALUES (gen_random_uuid(), %s, %s, %s, %s)"
        parameters = (orderId[0], itemList[row], items.items[row].quantity, binList[row])
        save = instance_conexion.register(cursor, sql, parameters)
        if not save:
            instance_conexion.revert_changes(pool)
            instance_conexion.close_conexion(cursor, pool)
            return None, None, None

        sql = "UPDATE public.stock_per_bin a SET a.quantity_reserved= s.quantity_reserved + %s WHERE item_id=%s AND bin_id=%s"
        parameters = (items.items[row].quantity, itemList[row], binList[row])
        save = instance_conexion.register(cursor, sql, parameters)
        if not save:
            instance_conexion.revert_changes(pool)
            instance_conexion.close_conexion(cursor, pool)
            return None, None, None
    
    sql = "INSERT INTO public.order_status_history(id_external, order_id, status, changed_by, changed_at) VALUES (gen_random_uuid(), %s, 1, %s, %s)"
    parameters = (orderId[0], userGet[0], date)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    save = instance_conexion.execute_change(pool)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None
    
    instance_conexion.close_conexion(cursor, pool)
    return save, orderId[1], date

def pickOrder(user: str, order: str):
    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)
    pool, cursor = instance_conexion.init_conexion()
    userGet = instance_conexion.one(cursor, sql, parameters)
    date = datetime.now()

    sql = "SELECT id FROM public.orders WHERE id_external=%s AND status=1 FOR UPDATE"
    parameters = (order,)
    orderGet = instance_conexion.one(cursor, sql, parameters)

    if orderGet == None:
        instance_conexion.close_conexion(cursor, pool)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The order has already picked up.")

    sql = "SELECT count(id) FROM public.order_items WHERE order_id=%s"
    parameters = (orderGet[0],)
    count = instance_conexion.one(cursor, sql, parameters)

    sql = "SELECT item_id, bin_id, quantity_requested FROM public.order_items WHERE order_id=%s"
    parameters = (orderGet[0],)
    dataGet = instance_conexion.all_parameters(cursor, sql, parameters)
    
    if count == None or dataGet == None:
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None
    
    for row in range(count[0]):
        sql = "SELECT id FROM public.stock_per_bin WHERE item_id=%s AND bin_id=%s FOR UPDATE"
        parameters = (dataGet[row][0], dataGet[row][1])
        stockGet = instance_conexion.one(cursor, sql, parameters)
            
        if count == None or dataGet == None:
            instance_conexion.revert_changes(pool)
            instance_conexion.close_conexion(cursor, pool)
            return None, None, None
        
        sql = "UPDATE public.stock_per_bin s SET quantity_available= s.quantity_available - %s, quantity_reserved= s.quantity_reserved - %s WHERE id=%s"
        parameters = (dataGet[row][2], dataGet[row][2], stockGet[0])
        save = instance_conexion.register(cursor, sql, parameters)
        if not save:
            instance_conexion.revert_changes(pool)
            instance_conexion.close_conexion(cursor, pool)
            return None, None, None

    sql = "INSERT INTO public.order_status_history(id_external, order_id, status, changed_by, changed_at) VALUES (gen_random_uuid(), %s, 2, %s, %s)"
    parameters = (orderGet[0], userGet[0], date)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    sql = "UPDATE public.orders SET status=2 WHERE id=%s"
    parameters = (orderGet[0],)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    save = instance_conexion.execute_change(pool)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None
    
    instance_conexion.close_conexion(cursor, pool)

    return save, order, date

def shipOrder(user: str, order: str):
    sql = "SELECT u.id FROM public.users u WHERE u.id_external=%s"
    parameters = (user,)
    pool, cursor = instance_conexion.init_conexion()
    userGet = instance_conexion.one(cursor, sql, parameters)
    date = datetime.now()

    sql = "SELECT id FROM public.orders WHERE id_external=%s AND status=2 FOR UPDATE"
    parameters = (order,)
    orderGet = instance_conexion.one(cursor, sql, parameters)

    if orderGet == None:
        instance_conexion.close_conexion(cursor, pool)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The order has already shipped.")

    sql = "INSERT INTO public.order_status_history(id_external, order_id, status, changed_by, changed_at) VALUES (gen_random_uuid(), %s, 3, %s, %s)"
    parameters = (orderGet[0], userGet[0], date)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    sql = "UPDATE public.orders SET status=3 WHERE id=%s"
    parameters = (orderGet[0],)
    save = instance_conexion.register(cursor, sql, parameters)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None

    save = instance_conexion.execute_change(pool)
    if not save:
        instance_conexion.revert_changes(pool)
        instance_conexion.close_conexion(cursor, pool)
        return None, None, None
    
    instance_conexion.close_conexion(cursor, pool)

    return save, order, date

def getOrderStatusHistoryPaginated(limit: int, offset: int, q: str | None = None):
    pool, cursor = instance_conexion.init_conexion()

    sql = """
        SELECT 
            osi.id_external, 
            u.username, 
            i.sku, 
            i.name, 
            oi.quantity_requested, 
            os.status,
            osi.changed_at, 
            b.generated_code
        FROM public.order_status_history osi 
        INNER JOIN public.users u ON osi.changed_by = u.id
        INNER JOIN public.order_status os ON osi.status=os.id
        INNER JOIN public.orders o ON osi.order_id = o.id
        INNER JOIN public.order_items oi ON o.id = oi.order_id 
        INNER JOIN public.items i ON oi.item_id = i.id
        INNER JOIN public.bins b ON oi.bin_id = b.id 
    """
    sql_count = """
        SELECT COUNT(*)
        FROM public.order_status_history osi 
        INNER JOIN public.users u ON osi.changed_by = u.id
        INNER JOIN public.order_status os ON osi.status=os.id
        INNER JOIN public.orders o ON osi.order_id = o.id
        INNER JOIN public.order_items oi ON o.id = oi.order_id 
        INNER JOIN public.items i ON oi.item_id = i.id
        INNER JOIN public.bins b ON oi.bin_id = b.id 
    """

    filters = []
    parameters = ()

    if q and q.strip() and q != "string":
        search_term = f"%{q.strip()}%"
        filters.append("(i.sku ILIKE %s OR i.name ILIKE %s OR u.username ILIKE %s OR osi.id_external ILIKE %s)")
        parameters += (search_term, search_term, search_term, search_term)

    if filters:
        where_clause = " WHERE " + " AND ".join(filters)
        sql += where_clause
        sql_count += where_clause

    sql += " ORDER BY osi.id DESC LIMIT %s OFFSET %s"

    count_parameters = parameters
    parameters += (limit, offset)

    rows = instance_conexion.all_parameters(cursor, sql, parameters)
    count_result = instance_conexion.one(cursor, sql_count, count_parameters)

    instance_conexion.close_conexion(cursor, pool) 

    return rows, count_result[0]