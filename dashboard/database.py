import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


@st.cache_resource
def get_engine():
    config = st.secrets["connections"]["postgresql"]

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=config["username"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["database"],
    )

    return create_engine(url, pool_pre_ping=True)