from repository.conexion_db import instance_conexion

def get_stock_movements_paginated(limit: int, offset: int, movement_type: str | None = None, item_id: str | None = None, movement_external_id: str | None = None):
    sql = """
        SELECT 
            sm.id_external, 
            u.username, 
            m.movement, 
            si.quantity, 
            i.name, 
            i.sku, 
            from_id.generated_code AS from_bin_code, 
            to_id.generated_code AS to_bin_code, 
            sm.created_at 
        FROM public.stock_movements sm 
        INNER JOIN public.users u ON sm.user_id = u.id 
        INNER JOIN public.movements m ON sm.action_type = m.id 
        INNER JOIN public.stock_movement_items si ON sm.id = si.movement_id
        INNER JOIN public.items i ON i.id = si.item_id 
        LEFT JOIN public.bins AS from_id ON from_id.id = si.from_bin_id
        LEFT JOIN public.bins AS to_id ON to_id.id = si.to_bin_id
    """
    sql_count = "SELECT COUNT(*) FROM public.stock_movements sm INNER JOIN public.users u ON sm.user_id = u.id  INNER JOIN public.movements m ON sm.action_type = m.id INNER JOIN public.stock_movement_items si ON sm.id = si.movement_id INNER JOIN public.items i ON i.id = si.item_id  LEFT JOIN public.bins AS from_id ON from_id.id = si.from_bin_id LEFT JOIN public.bins AS to_id ON to_id.id = si.to_bin_id "
    
    filters = []
    parameters = ()
    filters_count = []
    parameters_count = ()
    pool, cursor = instance_conexion.init_conexion()

    if movement_type is not None and movement_type != "" and movement_type != "string":
        filters.append("m.id_external = %s")
        filters_count.append("m.id_external = %s")
        parameters += (movement_type,)
        parameters_count += (movement_type,)

    if item_id is not None:
        filters.append("i.id_external = %s")
        filters_count.append("i.id_external = %s")
        parameters += (item_id,)
        parameters_count += (item_id,)

    if movement_external_id is not None and movement_external_id != "" and movement_external_id != "string":
        filters.append("sm.id_external = %s")
        filters_count.append("sm.id_external = %s")
        parameters += (movement_external_id,)
        parameters_count += (movement_external_id,)

    if filters:
        sql += " WHERE " + " AND ".join(filters)
        sql_count += " WHERE " + " AND ".join(filters_count)

    sql += " ORDER BY sm.id DESC LIMIT %s OFFSET %s;"
    parameters += (limit, offset)


    movements = instance_conexion.all_parameters(cursor, sql, parameters)
    count = instance_conexion.one(cursor, sql_count, parameters_count)
    
    instance_conexion.close_conexion(cursor, pool)

    return movements, count

def get_stock_per_bin_paginated(limit: int, offset: int, search_query: str | None = None, bin_code: str | None = None):
    sql = " SELECT i.sku, i.name, i.image, b.generated_code, sb.quantity_available, sb.quantity_reserved FROM public.stock_per_bin sb INNER JOIN public.items i ON sb.item_id = i.id INNER JOIN public.bins b ON sb.bin_id = b.id "
    
    sql_count = "SELECT COUNT(*) FROM public.stock_per_bin sb INNER JOIN public.items i ON sb.item_id = i.id INNER JOIN public.bins b ON sb.bin_id = b.id "
    
    filters = []
    parameters = ()
    filters_count = []
    parameters_count = ()
    
    pool, cursor = instance_conexion.init_conexion()

    if search_query is not None and search_query != "" and search_query != "string":
        filters.append("(i.sku ILIKE %s OR i.name ILIKE %s)")
        filters_count.append("(i.sku ILIKE %s OR i.name ILIKE %s)")
        parameters += (f"%{search_query}%", f"%{search_query}%")
        parameters_count += (f"%{search_query}%", f"%{search_query}%")

    if bin_code is not None and bin_code != "" and bin_code != "string":
        filters.append("b.generated_code ILIKE %s")
        filters_count.append("b.generated_code ILIKE %s")
        parameters += (f"%{bin_code}%",)
        parameters_count += (f"%{bin_code}%",)

    if filters:
        sql += " WHERE " + " AND ".join(filters)
        sql_count += " WHERE " + " AND ".join(filters_count)

    sql += " ORDER BY sb.id DESC LIMIT %s OFFSET %s;"
    parameters += (limit, offset)

    stock_records = instance_conexion.all_parameters(cursor, sql, parameters)
    count = instance_conexion.one(cursor, sql_count, parameters_count)
    
    instance_conexion.close_conexion(cursor, pool)

    return stock_records, count