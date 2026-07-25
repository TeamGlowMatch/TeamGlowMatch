import streamlit as st
import pyodbc
from google import genai
from db import run_query

st.set_page_config(page_title="GlowMatch", layout="wide")
st.title("Hello")

if st.button("Test Azure SQL Connection"):
    # Run a simple built-in SQL query to test connectivity
    test_df = run_query("SELECT * FROM Products")
    
    if not test_df.empty:
        st.success("Connected to Azure SQL successfully!")
        st.dataframe(test_df)




