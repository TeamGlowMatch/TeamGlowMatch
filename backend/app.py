import streamlit as st

st.set_page_config(
    page_title="GlowMatch",
    page_icon="logo.png",  # Points to your image file
    layout="wide",
)

# Declared pages
home_page = st.Page("pages/dashboard.py", title="Dashboard", icon="🏠", default=True)
ai_page = st.Page("pages/genAi_page.py", title="AI Assistant", icon="🤖")

# Register navigation
pg = st.navigation([home_page, ai_page])

# Shared sidebar elements (runs on every page)
with st.sidebar:
    st.image("logo.png", width="content")

# Render active page content
pg.run()