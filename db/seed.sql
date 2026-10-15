-- ==========================================
-- 1. BASE CATALOGS
-- ==========================================

INSERT INTO public.order_status (id_external, status) VALUES
  (gen_random_uuid(), 'PENDING'),
  (gen_random_uuid(), 'PICKED'),
  (gen_random_uuid(), 'SHIPPED')
ON CONFLICT (id_external) DO NOTHING;

INSERT INTO public.movements (id_external, movement) VALUES
  (gen_random_uuid(), 'RECEIVE'),
  (gen_random_uuid(), 'RECEIVE_NEW'),
  (gen_random_uuid(), 'MOVE')
ON CONFLICT (movement) DO NOTHING;

INSERT INTO public.user_roles (id_external, role_name) VALUES
  (gen_random_uuid(), 'Admin'),
  (gen_random_uuid(), 'Worker')
ON CONFLICT (role_name) DO NOTHING;

-- ==========================================
-- 2. INITIAL USERS
-- ==========================================

INSERT INTO public.users (id_external, username, password_hash, image, role_id) VALUES
  (
    gen_random_uuid(),
    'admin',
    '$pbkdf2-sha256$29000$.9.bk/K.1xojhBBizLl3Dg$DqgVy.lu/eLEWME5TwTcyPnvhh1bbAAsb5K284VE1Gk',
    'image_defect.png',
    (SELECT id FROM public.user_roles WHERE role_name = 'Admin' LIMIT 1)
  ),
  (
    gen_random_uuid(),
    'worker',
    '$pbkdf2-sha256$29000$.9.bk/K.1xojhBBizLl3Dg$DqgVy.lu/eLEWME5TwTcyPnvhh1bbAAsb5K284VE1Gk',
    'image_defect.png',
    (SELECT id FROM public.user_roles WHERE role_name = 'Worker' LIMIT 1)
  )
ON CONFLICT (username) DO NOTHING;

-- ==========================================
-- 3. BINS (PHYSICAL LOCATIONS)
-- ==========================================

INSERT INTO public.bins (id_external, aisle, bay, tier, "position", generated_code) VALUES
  (gen_random_uuid(), 1, 'C', 3, '03', '1-C-3-03'),
  (gen_random_uuid(), 1, 'B01', 1, 'P01', 'A1-B01-1-P01'),
  (gen_random_uuid(), 2, 'A', 2, '01', '2-A-2-01'),
  (gen_random_uuid(), 2, 'A', 2, '02', '2-A-2-02')
ON CONFLICT (generated_code) DO NOTHING;

-- ==========================================
-- 4. ITEMS (PRODUCT CATALOG)
-- ==========================================

INSERT INTO public.items (id_external, sku, name, image, description) VALUES
  (gen_random_uuid(), 'SHOVEL-ITEM-001', 'Shovel', '31550281-4b7f-4aa2-af9e-24732d7b47e2.png', 'Heavy duty construction shovel'),
  (gen_random_uuid(), 'LAM-ESC-NG-LED', 'lamp', '60d69a8a-693a-41f7-9003-3a65949fd4ee.png', 'Emergency LED desk lamp')
ON CONFLICT (sku) DO NOTHING;

-- ==========================================
-- 5. INITIAL STOCK PER BIN
-- ==========================================

INSERT INTO public.stock_per_bin (item_id, bin_id, quantity_available, quantity_reserved) VALUES
  (
    (SELECT id FROM public.items WHERE sku = 'SHOVEL-ITEM-001' LIMIT 1),
    (SELECT id FROM public.bins WHERE generated_code = '1-C-3-03' LIMIT 1),
    100, 0
  ),
  (
    (SELECT id FROM public.items WHERE sku = 'LAM-ESC-NG-LED' LIMIT 1),
    (SELECT id FROM public.bins WHERE generated_code = 'A1-B01-1-P01' LIMIT 1),
    50, 0
  )
ON CONFLICT (item_id, bin_id) DO NOTHING;

-- ==========================================
-- 6. EXAMPLE ORDERS
-- ==========================================

INSERT INTO public.orders (id_external, status, created_by) VALUES
  (
    'ca8aa5fa-182c-41e6-8ea5-a95386012808',
    (SELECT id FROM public.order_status WHERE status = 'SHIPPED' LIMIT 1),
    (SELECT id FROM public.users WHERE username = 'admin' LIMIT 1)
  )
ON CONFLICT (id_external) DO NOTHING;

-- Items associated with the order
INSERT INTO public.order_items (id_external, order_id, item_id, quantity_requested, bin_id) VALUES
  (
    gen_random_uuid(),
    (SELECT id FROM public.orders WHERE id_external = 'ca8aa5fa-182c-41e6-8ea5-a95386012808' LIMIT 1),
    (SELECT id FROM public.items WHERE sku = 'SHOVEL-ITEM-001' LIMIT 1),
    30,
    (SELECT id FROM public.bins WHERE generated_code = '1-C-3-03' LIMIT 1)
  ),
  (
    gen_random_uuid(),
    (SELECT id FROM public.orders WHERE id_external = 'ca8aa5fa-182c-41e6-8ea5-a95386012808' LIMIT 1),
    (SELECT id FROM public.items WHERE sku = 'LAM-ESC-NG-LED' LIMIT 1),
    20,
    (SELECT id FROM public.bins WHERE generated_code = 'A1-B01-1-P01' LIMIT 1)
  )
ON CONFLICT (id_external) DO NOTHING;

-- ==========================================
-- 7. ORDER STATUS HISTORY
-- ==========================================

INSERT INTO public.order_status_history (id_external, order_id, status, changed_by, changed_at) VALUES
  (
    gen_random_uuid(),
    (SELECT id FROM public.orders WHERE id_external = 'ca8aa5fa-182c-41e6-8ea5-a95386012808' LIMIT 1),
    (SELECT id FROM public.order_status WHERE status = 'SHIPPED' LIMIT 1),
    (SELECT id FROM public.users WHERE username = 'admin' LIMIT 1),
    '2026-10-12 15:08:34.412724'
  );

-- ==========================================
-- 8. STOCK MOVEMENTS (Logistics)
-- ==========================================

-- CASE A: RECEIVE_NEW
INSERT INTO public.stock_movements (id_external, user_id, action_type, created_at) VALUES
  (
    gen_random_uuid(),
    (SELECT id FROM public.users WHERE username = 'admin' LIMIT 1),
    (SELECT id FROM public.movements WHERE movement = 'RECEIVE_NEW' LIMIT 1),
    '2026-10-12 09:30:00'
  )
ON CONFLICT (id_external) DO NOTHING;

INSERT INTO public.stock_movement_items (movement_id, item_id, quantity, from_bin_id, to_bin_id) VALUES
  (
    (SELECT id FROM public.stock_movements WHERE created_at = '2026-10-12 09:30:00' LIMIT 1),
    (SELECT id FROM public.items WHERE sku = 'SHOVEL-ITEM-001' LIMIT 1),
    100,
    NULL,
    (SELECT id FROM public.bins WHERE generated_code = '1-C-3-03' LIMIT 1)
  );

-- CASE B: RECEIVE
INSERT INTO public.stock_movements (id_external, user_id, action_type, created_at) VALUES
  (
    gen_random_uuid(),
    (SELECT id FROM public.users WHERE username = 'admin' LIMIT 1),
    (SELECT id FROM public.movements WHERE movement = 'RECEIVE' LIMIT 1),
    '2026-10-12 11:00:00'
  )
ON CONFLICT (id_external) DO NOTHING;

INSERT INTO public.stock_movement_items (movement_id, item_id, quantity, from_bin_id, to_bin_id) VALUES
  (
    (SELECT id FROM public.stock_movements WHERE created_at = '2026-10-12 11:00:00' LIMIT 1),
    (SELECT id FROM public.items WHERE sku = 'LAM-ESC-NG-LED' LIMIT 1),
    50,
    NULL,
    (SELECT id FROM public.bins WHERE generated_code = 'A1-B01-1-P01' LIMIT 1)
  );

-- CASE C: MOVE
INSERT INTO public.stock_movements (id_external, user_id, action_type, created_at) VALUES
  (
    gen_random_uuid(),
    (SELECT id FROM public.users WHERE username = 'admin' LIMIT 1),
    (SELECT id FROM public.movements WHERE movement = 'MOVE' LIMIT 1),
    '2026-10-12 16:15:00'
  )
ON CONFLICT (id_external) DO NOTHING;

INSERT INTO public.stock_movement_items (movement_id, item_id, quantity, from_bin_id, to_bin_id) VALUES
  (
    (SELECT id FROM public.stock_movements WHERE created_at = '2026-10-12 16:15:00' LIMIT 1),
    (SELECT id FROM public.items WHERE sku = 'LAM-ESC-NG-LED' LIMIT 1),
    10,
    (SELECT id FROM public.bins WHERE generated_code = 'A1-B01-1-P01' LIMIT 1),
    (SELECT id FROM public.bins WHERE generated_code = '1-C-3-03' LIMIT 1)
  );