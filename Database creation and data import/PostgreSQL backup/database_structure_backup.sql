--
-- PostgreSQL database dump
--

-- Dumped from database version 10.0
-- Dumped by pg_dump version 10.0

-- Started on 2017-11-20 11:07:12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 20319)
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- TOC entry 4341 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 4342 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 2 (class 3079 OID 18820)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 4343 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 3 (class 3079 OID 20320)
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- TOC entry 4344 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 220 (class 1259 OID 48705)
-- Name: loype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE loype (
    tid timestamp with time zone NOT NULL,
    punkt geometry(Point,4326)
);


ALTER TABLE loype OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 48852)
-- Name: simulering; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE simulering (
    id integer NOT NULL,
    tid timestamp with time zone NOT NULL,
    punkt geometry(Point,4326)
);


ALTER TABLE simulering OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 48850)
-- Name: simulering_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE simulering_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE simulering_id_seq OWNER TO postgres;

--
-- TOC entry 4345 (class 0 OID 0)
-- Dependencies: 221
-- Name: simulering_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE simulering_id_seq OWNED BY simulering.id;


--
-- TOC entry 4202 (class 2604 OID 48855)
-- Name: simulering id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY simulering ALTER COLUMN id SET DEFAULT nextval('simulering_id_seq'::regclass);


--
-- TOC entry 4204 (class 2606 OID 48712)
-- Name: loype loype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY loype
    ADD CONSTRAINT loype_pkey PRIMARY KEY (tid);


--
-- TOC entry 4206 (class 2606 OID 48860)
-- Name: simulering simulering_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY simulering
    ADD CONSTRAINT simulering_pkey PRIMARY KEY (tid);


-- Completed on 2017-11-20 11:07:14

--
-- PostgreSQL database dump complete
--

