--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: category; Type: TABLE; Schema: public; Owner: waikup; Tablespace:
--

CREATE TABLE category (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.category OWNER TO waikup;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.category_id_seq OWNER TO waikup;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: link; Type: TABLE; Schema: public; Owner: waikup; Tablespace:
--

CREATE TABLE link (
    id integer NOT NULL,
    url character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    submitted timestamp without time zone NOT NULL,
    archived boolean NOT NULL,
    author_id integer NOT NULL,
    category_id integer
);


ALTER TABLE public.link OWNER TO waikup;

--
-- Name: link_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.link_id_seq OWNER TO waikup;

--
-- Name: link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE link_id_seq OWNED BY link.id;


--
-- Name: token; Type: TABLE; Schema: public; Owner: waikup; Tablespace:
--

CREATE TABLE token (
    id integer NOT NULL,
    token character varying(255) NOT NULL,
    user_id integer NOT NULL,
    expiry timestamp without time zone NOT NULL
);


ALTER TABLE public.token OWNER TO waikup;

--
-- Name: token_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_id_seq OWNER TO waikup;

--
-- Name: token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE token_id_seq OWNED BY token.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: waikup; Tablespace:
--

CREATE TABLE "user" (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    admin boolean NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public."user" OWNER TO waikup;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO waikup;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY link ALTER COLUMN id SET DEFAULT nextval('link_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY token ALTER COLUMN id SET DEFAULT nextval('token_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY category (id, name) FROM stdin;
1	Web
2	Forensics
3	Reverse Engineering
4	Cryptography
5	Networking
6	Development
7	Malware
8	News
9	Fun
10	Other
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('category_id_seq', 10, true);


--
-- Data for Name: link; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY link (id, url, title, description, submitted, archived, author_id, category_id) FROM stdin;
1	http://example.com/1	link 1 title	link 1 desc	2014-05-24 19:53:25.662822	f	1	1
2	http://example.com/2	link 2 title	link 2 desc	2014-05-24 19:53:51.048588	f	1	2
3	http://example.com/3	link 3 title	link 3 desc	2014-05-24 19:54:31.527977	f	3	3
\.


--
-- Name: link_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('link_id_seq', 3, true);


--
-- Data for Name: token; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY token (id, token, user_id, expiry) FROM stdin;
1	72099f7109c87d275fd51a4f9c474d28	2	2014-05-31 14:11:35.578912
\.


--
-- Name: token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('token_id_seq', 1, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY "user" (id, username, first_name, last_name, password, email, admin, active) FROM stdin;
1	admin	WaikUp	Admin	pbkdf2:sha256:2000$7YlehPMMiIlxtBvz$d5b80fd023986192a5babaebd3ec4d264b3011ac6acfd38e3da1848ce4b26c6b	admin@example.org	t	t
2	waikupapi	WaikUp	API	pbkdf2:sha256:2000$Iz6TXlakxVE9IkMo$392e2400db67be604fb27eef0d609be71af060c086904d4642c3db90f6683172	api@example.org	f	t
3	user	Test	User	pbkdf2:sha256:2000$SjGXdMsfrp5wJDUb$8fb166e9f550f7c5cb37456dbe033670f084acb429aa7ae357dff3aa162f30cc	testuser@example.com	f	t
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('user_id_seq', 3, true);


--
-- Name: category_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup; Tablespace:
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: link_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup; Tablespace:
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_pkey PRIMARY KEY (id);


--
-- Name: token_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup; Tablespace:
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup; Tablespace:
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: category_name; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE UNIQUE INDEX category_name ON category USING btree (name);


--
-- Name: link_author_id; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE INDEX link_author_id ON link USING btree (author_id);


--
-- Name: link_category_id; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE INDEX link_category_id ON link USING btree (category_id);


--
-- Name: link_url; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE UNIQUE INDEX link_url ON link USING btree (url);


--
-- Name: token_user_id; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE UNIQUE INDEX token_user_id ON token USING btree (user_id);


--
-- Name: user_username; Type: INDEX; Schema: public; Owner: waikup; Tablespace:
--

CREATE UNIQUE INDEX user_username ON "user" USING btree (username);


--
-- Name: link_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_author_id_fkey FOREIGN KEY (author_id) REFERENCES "user"(id);


--
-- Name: link_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: token_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
