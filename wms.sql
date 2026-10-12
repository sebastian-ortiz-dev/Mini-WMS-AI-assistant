CREATE TABLE "user_roles" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "role_name" varchar(50) UNIQUE NOT NULL
);

CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "username" varchar(100) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "role_id" int NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "items" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "sku" varchar(150) UNIQUE NOT NULL,
  "name" varchar(100) NOT NULL,
  "image" varchar(250) NOT NULL,
  "description" text,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "bins" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "aisle" int NOT NULL,
  "bay" varchar(10) NOT NULL,
  "tier" int NOT NULL,
  "position" varchar(10) NOT NULL,
  "generated_code" varchar(50) UNIQUE NOT NULL
);

CREATE TABLE "stock_per_bin" (
  "id" serial PRIMARY KEY NOT NULL,
  "item_id" int NOT NULL,
  "bin_id" int NOT NULL,
  "quantity_available" int NOT NULL DEFAULT 0,
  "quantity_reserved" int NOT NULL DEFAULT 0,
  CONSTRAINT chk_quantity_available CHECK ("quantity_available" >= 0),
  CONSTRAINT chk_quantity_reserved CHECK ("quantity_reserved" >= 0),
  CONSTRAINT uq_item_bin UNIQUE ("item_id", "bin_id")
);

CREATE TABLE "orders" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "status" int NOT NULL,
  "created_by" int NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "order_status" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "status" varchar(50) NOT NULL
);

CREATE TABLE "order_items" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "order_id" int NOT NULL,
  "item_id" int NOT NULL,
  "quantity_requested" int NOT NULL
);

CREATE TABLE "order_status_history" (
  "id" serial PRIMARY KEY,
  "order_id" int NOT NULL,
  "status" int NOT NULL,
  "changed_by" int NOT NULL,
  "changed_at" timestamp DEFAULT (now())
);

CREATE TABLE "stock_movements" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "user_id" int NOT NULL,
  "action_type" int NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "movements" (
  "id" serial PRIMARY KEY,
  "id_external" varchar(100) UNIQUE NOT NULL,
  "movement" varchar(100) UNIQUE NOT NULL
);

CREATE TABLE "stock_movement_items" (
  "id" serial PRIMARY KEY,
  "movement_id" int NOT NULL,
  "item_id" int NOT NULL,
  "quantity" int NOT NULL,
  "from_bin_id" int,
  "to_bin_id" int,
  CONSTRAINT chk_quantity CHECK ("quantity" >= 0)
);

COMMENT ON TABLE "stock_per_bin" IS 'Composite primary key (item_id, bin_id). Strict transactional database constraints applied here.';

COMMENT ON TABLE "stock_movements" IS 'Cabecera de los movimientos logísticos y de inventario físico en el almacén.';

COMMENT ON TABLE "stock_movement_items" IS 'Subtabla con los detalles (renglones) de cada ítem afectado en el movimiento físico.';

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "user_roles" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_per_bin" ADD FOREIGN KEY ("item_id") REFERENCES "items" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_per_bin" ADD FOREIGN KEY ("bin_id") REFERENCES "bins" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "orders" ADD FOREIGN KEY ("status") REFERENCES "order_status" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "orders" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_items" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_items" ADD FOREIGN KEY ("item_id") REFERENCES "items" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_status_history" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_status_history" ADD FOREIGN KEY ("status") REFERENCES "order_status" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_status_history" ADD FOREIGN KEY ("changed_by") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movements" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movements" ADD FOREIGN KEY ("action_type") REFERENCES "movements" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movement_items" ADD FOREIGN KEY ("movement_id") REFERENCES "stock_movements" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movement_items" ADD FOREIGN KEY ("item_id") REFERENCES "items" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movement_items" ADD FOREIGN KEY ("from_bin_id") REFERENCES "bins" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "stock_movement_items" ADD FOREIGN KEY ("to_bin_id") REFERENCES "bins" ("id") DEFERRABLE INITIALLY IMMEDIATE;
