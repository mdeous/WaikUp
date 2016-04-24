--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

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
-- Name: category; Type: TABLE; Schema: public; Owner: waikup
--

CREATE TABLE category (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE category OWNER TO waikup;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE category_id_seq OWNER TO waikup;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: email; Type: TABLE; Schema: public; Owner: waikup
--

CREATE TABLE email (
    id integer NOT NULL,
    address character varying(255) NOT NULL,
    disabled boolean NOT NULL
);


ALTER TABLE email OWNER TO waikup;

--
-- Name: email_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE email_id_seq OWNER TO waikup;

--
-- Name: email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE email_id_seq OWNED BY email.id;


--
-- Name: link; Type: TABLE; Schema: public; Owner: waikup
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


ALTER TABLE link OWNER TO waikup;

--
-- Name: link_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE link_id_seq OWNER TO waikup;

--
-- Name: link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE link_id_seq OWNED BY link.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: waikup
--

CREATE TABLE role (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE role OWNER TO waikup;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE role_id_seq OWNER TO waikup;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE role_id_seq OWNED BY role.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: waikup
--

CREATE TABLE "user" (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    admin boolean NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE "user" OWNER TO waikup;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO waikup;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: userrole; Type: TABLE; Schema: public; Owner: waikup
--

CREATE TABLE userrole (
    id integer NOT NULL,
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE userrole OWNER TO waikup;

--
-- Name: userrole_id_seq; Type: SEQUENCE; Schema: public; Owner: waikup
--

CREATE SEQUENCE userrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userrole_id_seq OWNER TO waikup;

--
-- Name: userrole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: waikup
--

ALTER SEQUENCE userrole_id_seq OWNED BY userrole.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY email ALTER COLUMN id SET DEFAULT nextval('email_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY link ALTER COLUMN id SET DEFAULT nextval('link_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY role ALTER COLUMN id SET DEFAULT nextval('role_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY userrole ALTER COLUMN id SET DEFAULT nextval('userrole_id_seq'::regclass);


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
-- Data for Name: email; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY email (id, address, disabled) FROM stdin;
\.


--
-- Name: email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('email_id_seq', 1, false);


--
-- Data for Name: link; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY link (id, url, title, description, submitted, archived, author_id, category_id) FROM stdin;
6	http://blablablbgksrlnbgda.com	some title 1	description 1	2016-04-19 22:26:16.545764	f	1	6
4	http://blablabla.com	some title 2	description 2	2016-04-19 22:20:32.034708	f	1	3
2	http://blabla.com	some title 3	description 3	2016-04-19 22:16:29.026549	f	1	7
1	http://test.com/bla	some title 4	description 4	2016-04-18 23:34:48.045487	f	1	5
5	http://blablablbgksrbgda.com	some title	description	2016-04-19 22:24:42.691532	t	1	9
\.


--
-- Name: link_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('link_id_seq', 6, true);


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY role (id, name, description) FROM stdin;
\.


--
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('role_id_seq', 1, false);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY "user" (id, first_name, last_name, password, email, admin, active) FROM stdin;
1	admin	admin	$pbkdf2-sha512$25000$a63VWmvtHUPIeY/xPue8tw$lpiFwO18/pbHGxN3f0KRlLv.QgWt9mrnHUT5OEbvh6gHgEcnR824TtQdG.Oo4dYYbOZheLzbyZqdULIVa8bzpg	admin@example.com	t	t
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('user_id_seq', 1, true);


--
-- Data for Name: userrole; Type: TABLE DATA; Schema: public; Owner: waikup
--

COPY userrole (id, user_id, role_id) FROM stdin;
\.


--
-- Name: userrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: waikup
--

SELECT pg_catalog.setval('userrole_id_seq', 1, false);


--
-- Name: category_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: email_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY email
    ADD CONSTRAINT email_pkey PRIMARY KEY (id);


--
-- Name: link_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_pkey PRIMARY KEY (id);


--
-- Name: role_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: userrole_pkey; Type: CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY userrole
    ADD CONSTRAINT userrole_pkey PRIMARY KEY (id);


--
-- Name: category_name; Type: INDEX; Schema: public; Owner: waikup
--

CREATE UNIQUE INDEX category_name ON category USING btree (name);


--
-- Name: email_address; Type: INDEX; Schema: public; Owner: waikup
--

CREATE UNIQUE INDEX email_address ON email USING btree (address);


--
-- Name: link_author_id; Type: INDEX; Schema: public; Owner: waikup
--

CREATE INDEX link_author_id ON link USING btree (author_id);


--
-- Name: link_category_id; Type: INDEX; Schema: public; Owner: waikup
--

CREATE INDEX link_category_id ON link USING btree (category_id);


--
-- Name: link_url; Type: INDEX; Schema: public; Owner: waikup
--

CREATE UNIQUE INDEX link_url ON link USING btree (url);


--
-- Name: role_name; Type: INDEX; Schema: public; Owner: waikup
--

CREATE UNIQUE INDEX role_name ON role USING btree (name);


--
-- Name: user_email; Type: INDEX; Schema: public; Owner: waikup
--

CREATE UNIQUE INDEX user_email ON "user" USING btree (email);


--
-- Name: userrole_role_id; Type: INDEX; Schema: public; Owner: waikup
--

CREATE INDEX userrole_role_id ON userrole USING btree (role_id);


--
-- Name: userrole_user_id; Type: INDEX; Schema: public; Owner: waikup
--

CREATE INDEX userrole_user_id ON userrole USING btree (user_id);


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
-- Name: userrole_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY userrole
    ADD CONSTRAINT userrole_role_id_fkey FOREIGN KEY (role_id) REFERENCES role(id);


--
-- Name: userrole_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: waikup
--

ALTER TABLE ONLY userrole
    ADD CONSTRAINT userrole_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


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

