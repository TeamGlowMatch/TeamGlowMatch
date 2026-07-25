# db.py
import streamlit as st
import pyodbc
import pandas as pd

@st.cache_resource
def get_connection():
    """Establishes and caches the connection to Azure SQL Server."""
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={st.secrets['azure']['server']};"
            f"DATABASE={st.secrets['azure']['database']};"
            f"UID={st.secrets['azure']['username']};"
            f"PWD={st.secrets['azure']['password']};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        return pyodbc.connect(connection_string)
    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return None

def run_query(query, params=()):
    """Executes a SQL query and returns the results as a Pandas DataFrame."""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        # Use Pandas to read the SQL query directly into a DataFrame
        return pd.read_sql(query, conn, params=params)
    except Exception as e:
        st.error(f"Query Execution Error: {e}")
        return pd.DataFrame()