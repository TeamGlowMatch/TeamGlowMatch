import streamlit as st

# Declared pages
home_page = st.Page("pages/dashboard.py", title="Dashboard", icon="🏠", default=True)
ai_page = st.Page("pages/genAi_page.py", title="AI Assistant", icon="🤖")

# Register navigation
pg = st.navigation([home_page, ai_page])

# Shared sidebar elements (runs on every page)
with st.sidebar:
    st.write("GlowMatch")

# Render active page content
pg.run()