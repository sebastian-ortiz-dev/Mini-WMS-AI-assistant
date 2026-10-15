--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2026-10-15 14:01:10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 131403)
-- Name: bins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bins (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    aisle integer NOT NULL,
    bay character varying(10) NOT NULL,
    tier integer NOT NULL,
    "position" character varying(10) NOT NULL,
    generated_code character varying(50) NOT NULL
);


--
-- TOC entry 223 (class 1259 OID 131402)
-- Name: bins_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5043 (class 0 OID 0)
-- Dependencies: 223
-- Name: bins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bins_id_seq OWNED BY public.bins.id;


--
-- TOC entry 222 (class 1259 OID 131389)
-- Name: items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.items (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    sku character varying(150) NOT NULL,
    name character varying(100) NOT NULL,
    image character varying(250) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT now()
);


--
-- TOC entry 221 (class 1259 OID 131388)
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5045 (class 0 OID 0)
-- Dependencies: 221
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- TOC entry 238 (class 1259 OID 131473)
-- Name: movements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.movements (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    movement character varying(100) NOT NULL
);


--
-- TOC entry 237 (class 1259 OID 131472)
-- Name: movements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5047 (class 0 OID 0)
-- Dependencies: 237
-- Name: movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.movements_id_seq OWNED BY public.movements.id;


--
-- TOC entry 232 (class 1259 OID 131446)
-- Name: order_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    order_id integer NOT NULL,
    item_id integer NOT NULL,
    quantity_requested integer NOT NULL,
    bin_id integer NOT NULL
);


--
-- TOC entry 231 (class 1259 OID 131445)
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5049 (class 0 OID 0)
-- Dependencies: 231
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- TOC entry 230 (class 1259 OID 131437)
-- Name: order_status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_status (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    status character varying(50) NOT NULL
);


--
-- TOC entry 234 (class 1259 OID 131455)
-- Name: order_status_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_status_history (
    id integer NOT NULL,
    id_external character varying(100) DEFAULT gen_random_uuid() NOT NULL,
    order_id integer NOT NULL,
    status integer NOT NULL,
    changed_by integer NOT NULL,
    changed_at timestamp without time zone DEFAULT now()
);


--
-- TOC entry 233 (class 1259 OID 131454)
-- Name: order_status_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_status_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 233
-- Name: order_status_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_status_history_id_seq OWNED BY public.order_status_history.id;


--
-- TOC entry 229 (class 1259 OID 131436)
-- Name: order_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 229
-- Name: order_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_status_id_seq OWNED BY public.order_status.id;


--
-- TOC entry 228 (class 1259 OID 131427)
-- Name: orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    status integer NOT NULL,
    created_by integer NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


--
-- TOC entry 227 (class 1259 OID 131426)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 227
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 240 (class 1259 OID 131484)
-- Name: stock_movement_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_movement_items (
    id integer NOT NULL,
    movement_id integer NOT NULL,
    item_id integer NOT NULL,
    quantity integer NOT NULL,
    from_bin_id integer,
    to_bin_id integer,
    CONSTRAINT chk_quantity CHECK ((quantity >= 0))
);


--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE stock_movement_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.stock_movement_items IS 'Subtabla con los detalles (renglones) de cada ítem afectado en el movimiento físico.';


--
-- TOC entry 239 (class 1259 OID 131483)
-- Name: stock_movement_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_movement_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 239
-- Name: stock_movement_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_movement_items_id_seq OWNED BY public.stock_movement_items.id;


--
-- TOC entry 236 (class 1259 OID 131463)
-- Name: stock_movements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_movements (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    user_id integer NOT NULL,
    action_type integer NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE stock_movements; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.stock_movements IS 'Cabecera de los movimientos logísticos y de inventario físico en el almacén.';


--
-- TOC entry 235 (class 1259 OID 131462)
-- Name: stock_movements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 235
-- Name: stock_movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_movements_id_seq OWNED BY public.stock_movements.id;


--
-- TOC entry 226 (class 1259 OID 131414)
-- Name: stock_per_bin; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_per_bin (
    id integer NOT NULL,
    item_id integer NOT NULL,
    bin_id integer NOT NULL,
    quantity_available integer DEFAULT 0 NOT NULL,
    quantity_reserved integer DEFAULT 0 NOT NULL,
    CONSTRAINT chk_quantity_available CHECK ((quantity_available >= 0)),
    CONSTRAINT chk_quantity_reserved CHECK ((quantity_reserved >= 0))
);


--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE stock_per_bin; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.stock_per_bin IS 'Composite primary key (item_id, bin_id). Strict transactional database constraints applied here.';


--
-- TOC entry 225 (class 1259 OID 131413)
-- Name: stock_per_bin_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_per_bin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 225
-- Name: stock_per_bin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_per_bin_id_seq OWNED BY public.stock_per_bin.id;


--
-- TOC entry 218 (class 1259 OID 131364)
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    role_name character varying(50) NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 131363)
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- TOC entry 220 (class 1259 OID 131375)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    id_external character varying(100) NOT NULL,
    username character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    image character varying(250) NOT NULL,
    role_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


--
-- TOC entry 219 (class 1259 OID 131374)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4803 (class 2604 OID 131406)
-- Name: bins id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bins ALTER COLUMN id SET DEFAULT nextval('public.bins_id_seq'::regclass);


--
-- TOC entry 4801 (class 2604 OID 131392)
-- Name: items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- TOC entry 4816 (class 2604 OID 131476)
-- Name: movements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movements ALTER COLUMN id SET DEFAULT nextval('public.movements_id_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 131449)
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 131440)
-- Name: order_status id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status ALTER COLUMN id SET DEFAULT nextval('public.order_status_id_seq'::regclass);


--
-- TOC entry 4811 (class 2604 OID 131458)
-- Name: order_status_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history ALTER COLUMN id SET DEFAULT nextval('public.order_status_history_id_seq'::regclass);


--
-- TOC entry 4807 (class 2604 OID 131430)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 4817 (class 2604 OID 131487)
-- Name: stock_movement_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items ALTER COLUMN id SET DEFAULT nextval('public.stock_movement_items_id_seq'::regclass);


--
-- TOC entry 4814 (class 2604 OID 131466)
-- Name: stock_movements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements ALTER COLUMN id SET DEFAULT nextval('public.stock_movements_id_seq'::regclass);


--
-- TOC entry 4804 (class 2604 OID 131417)
-- Name: stock_per_bin id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_per_bin ALTER COLUMN id SET DEFAULT nextval('public.stock_per_bin_id_seq'::regclass);


--
-- TOC entry 4798 (class 2604 OID 131367)
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- TOC entry 4799 (class 2604 OID 131378)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4840 (class 2606 OID 131412)
-- Name: bins bins_generated_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bins
    ADD CONSTRAINT bins_generated_code_key UNIQUE (generated_code);


--
-- TOC entry 4842 (class 2606 OID 131410)
-- Name: bins bins_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bins
    ADD CONSTRAINT bins_id_external_key UNIQUE (id_external);


--
-- TOC entry 4844 (class 2606 OID 131408)
-- Name: bins bins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bins
    ADD CONSTRAINT bins_pkey PRIMARY KEY (id);


--
-- TOC entry 4834 (class 2606 OID 131399)
-- Name: items items_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_id_external_key UNIQUE (id_external);


--
-- TOC entry 4836 (class 2606 OID 131397)
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- TOC entry 4838 (class 2606 OID 131401)
-- Name: items items_sku_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_sku_key UNIQUE (sku);


--
-- TOC entry 4868 (class 2606 OID 131480)
-- Name: movements movements_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movements
    ADD CONSTRAINT movements_id_external_key UNIQUE (id_external);


--
-- TOC entry 4870 (class 2606 OID 131482)
-- Name: movements movements_movement_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movements
    ADD CONSTRAINT movements_movement_key UNIQUE (movement);


--
-- TOC entry 4872 (class 2606 OID 131478)
-- Name: movements movements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movements
    ADD CONSTRAINT movements_pkey PRIMARY KEY (id);


--
-- TOC entry 4858 (class 2606 OID 131453)
-- Name: order_items order_items_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_id_external_key UNIQUE (id_external);


--
-- TOC entry 4860 (class 2606 OID 131451)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 4862 (class 2606 OID 131461)
-- Name: order_status_history order_status_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT order_status_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4854 (class 2606 OID 131444)
-- Name: order_status order_status_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_id_external_key UNIQUE (id_external);


--
-- TOC entry 4856 (class 2606 OID 131442)
-- Name: order_status order_status_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_pkey PRIMARY KEY (id);


--
-- TOC entry 4850 (class 2606 OID 131435)
-- Name: orders orders_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_id_external_key UNIQUE (id_external);


--
-- TOC entry 4852 (class 2606 OID 131433)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4874 (class 2606 OID 131490)
-- Name: stock_movement_items stock_movement_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items
    ADD CONSTRAINT stock_movement_items_pkey PRIMARY KEY (id);


--
-- TOC entry 4864 (class 2606 OID 131471)
-- Name: stock_movements stock_movements_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_id_external_key UNIQUE (id_external);


--
-- TOC entry 4866 (class 2606 OID 131469)
-- Name: stock_movements stock_movements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_pkey PRIMARY KEY (id);


--
-- TOC entry 4846 (class 2606 OID 131423)
-- Name: stock_per_bin stock_per_bin_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_per_bin
    ADD CONSTRAINT stock_per_bin_pkey PRIMARY KEY (id);


--
-- TOC entry 4848 (class 2606 OID 139389)
-- Name: stock_per_bin uq_item_bin; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_per_bin
    ADD CONSTRAINT uq_item_bin UNIQUE (item_id, bin_id);


--
-- TOC entry 4822 (class 2606 OID 131371)
-- Name: user_roles user_roles_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_id_external_key UNIQUE (id_external);


--
-- TOC entry 4824 (class 2606 OID 131369)
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4826 (class 2606 OID 131373)
-- Name: user_roles user_roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_name_key UNIQUE (role_name);


--
-- TOC entry 4828 (class 2606 OID 131385)
-- Name: users users_id_external_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_external_key UNIQUE (id_external);


--
-- TOC entry 4830 (class 2606 OID 131383)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4832 (class 2606 OID 131387)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4880 (class 2606 OID 147580)
-- Name: order_items order_bin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_bin_id_fkey FOREIGN KEY (bin_id) REFERENCES public.bins(id) NOT VALID;


--
-- TOC entry 4881 (class 2606 OID 131521)
-- Name: order_items order_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id) DEFERRABLE;


--
-- TOC entry 4882 (class 2606 OID 131516)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) DEFERRABLE;


--
-- TOC entry 4883 (class 2606 OID 131536)
-- Name: order_status_history order_status_history_changed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT order_status_history_changed_by_fkey FOREIGN KEY (changed_by) REFERENCES public.users(id) DEFERRABLE;


--
-- TOC entry 4884 (class 2606 OID 131526)
-- Name: order_status_history order_status_history_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT order_status_history_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) DEFERRABLE;


--
-- TOC entry 4885 (class 2606 OID 131531)
-- Name: order_status_history order_status_history_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_status_history
    ADD CONSTRAINT order_status_history_status_fkey FOREIGN KEY (status) REFERENCES public.order_status(id) DEFERRABLE;


--
-- TOC entry 4878 (class 2606 OID 131511)
-- Name: orders orders_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id) DEFERRABLE;


--
-- TOC entry 4879 (class 2606 OID 131506)
-- Name: orders orders_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_status_fkey FOREIGN KEY (status) REFERENCES public.order_status(id) DEFERRABLE;


--
-- TOC entry 4888 (class 2606 OID 131561)
-- Name: stock_movement_items stock_movement_items_from_bin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items
    ADD CONSTRAINT stock_movement_items_from_bin_id_fkey FOREIGN KEY (from_bin_id) REFERENCES public.bins(id) DEFERRABLE;


--
-- TOC entry 4889 (class 2606 OID 131556)
-- Name: stock_movement_items stock_movement_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items
    ADD CONSTRAINT stock_movement_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id) DEFERRABLE;


--
-- TOC entry 4890 (class 2606 OID 131551)
-- Name: stock_movement_items stock_movement_items_movement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items
    ADD CONSTRAINT stock_movement_items_movement_id_fkey FOREIGN KEY (movement_id) REFERENCES public.stock_movements(id) DEFERRABLE;


--
-- TOC entry 4891 (class 2606 OID 131566)
-- Name: stock_movement_items stock_movement_items_to_bin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement_items
    ADD CONSTRAINT stock_movement_items_to_bin_id_fkey FOREIGN KEY (to_bin_id) REFERENCES public.bins(id) DEFERRABLE;


--
-- TOC entry 4886 (class 2606 OID 131546)
-- Name: stock_movements stock_movements_action_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_action_type_fkey FOREIGN KEY (action_type) REFERENCES public.movements(id) DEFERRABLE;


--
-- TOC entry 4887 (class 2606 OID 131541)
-- Name: stock_movements stock_movements_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE;


--
-- TOC entry 4876 (class 2606 OID 131501)
-- Name: stock_per_bin stock_per_bin_bin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_per_bin
    ADD CONSTRAINT stock_per_bin_bin_id_fkey FOREIGN KEY (bin_id) REFERENCES public.bins(id) DEFERRABLE;


--
-- TOC entry 4877 (class 2606 OID 131496)
-- Name: stock_per_bin stock_per_bin_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_per_bin
    ADD CONSTRAINT stock_per_bin_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id) DEFERRABLE;


--
-- TOC entry 4875 (class 2606 OID 131491)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.user_roles(id) DEFERRABLE;


--
-- TOC entry 5042 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE bins; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.bins TO ia_agent;


--
-- TOC entry 5044 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE items; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.items TO ia_agent;


--
-- TOC entry 5046 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE movements; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.movements TO ia_agent;


--
-- TOC entry 5048 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE order_items; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.order_items TO ia_agent;


--
-- TOC entry 5050 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE order_status; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.order_status TO ia_agent;


--
-- TOC entry 5051 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE order_status_history; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.order_status_history TO ia_agent;


--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE orders; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.orders TO ia_agent;


--
-- TOC entry 5057 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE stock_movement_items; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.stock_movement_items TO ia_agent;


--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE stock_movements; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.stock_movements TO ia_agent;


--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE stock_per_bin; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.stock_per_bin TO ia_agent;


--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE user_roles; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.user_roles TO ia_agent;


--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE users; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.users TO ia_agent;


--
-- TOC entry 2099 (class 826 OID 155773)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: -
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO ia_agent;


-- Completed on 2026-10-15 14:01:11

--
-- PostgreSQL database dump complete
--

