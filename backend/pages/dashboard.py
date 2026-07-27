import streamlit as st
import pandas as pd
from db import run_query

st.title("GlowMatch: Clinical Skincare Portal")
st.write("Explore dermatological data, track patient usage logs, and run real-time analytics.")
st.divider()

# Create structured tabs for the demo
tab_sql, tab_logs, tab_explorer = st.tabs([
    "⚡ Live SQL Analytics", 
    "📝 Patient Skincare Logs", 
    "🔍 Database Explorer"
])

# =====================================================================
# TAB 1: THE 5 MANDATORY SQL QUERIES 
# =====================================================================
with tab_sql:
    st.header(" Live SQL Query Execution", text_alignment="center")
    st.write("Click any button below to execute the query in real-time against Azure SQL and view the raw syntax.")
    
    # --- WHERE QUERY 1 ---
    st.subheader("1. Filter Serums from Products")
    sql_where_1 = """SELECT Brand,Name,Type,Country
FROM dbo.Products
WHERE Type='Serum';"""
    st.code(sql_where_1, language="sql")
    if st.button("Run Query #1"):
        st.dataframe(run_query(sql_where_1))
    st.divider()
    
    # --- WHERE QUERY 2 ---
    st.subheader("2. High Popularity Brands (>90)")
    sql_where_2 = """SELECT Brand_Name,Popularity_Score,Country
FROM dbo.Brands
WHERE Popularity_Score>90;"""
    st.code(sql_where_2, language="sql")
    if st.button("Run Query #2"):
        st.dataframe(run_query(sql_where_2))
    st.divider()
    
    # --- WHERE QUERY 3 ---
    st.subheader("3. Active Ingredients & Hydration Levels")
    sql_where_3 = """SELECT Ingredient_Name,Main_Role,Hydration_Level
FROM dbo.Ingredients
WHERE Is_Active_Ingredient=1;"""
    st.code(sql_where_3, language="sql")
    if st.button("Run Query #3"):
        st.dataframe(run_query(sql_where_3))
    st.divider()
    
    # --- HAVING QUERY 1 ---
    st.subheader("4. Countries with Multiple Brands (≥2)")
    sql_having_1 = """SELECT Country,COUNT(Brand) AS Numar_Branduri
FROM dbo.Products
GROUP BY Country
HAVING COUNT(Brand)>=2
ORDER BY Numar_Branduri DESC"""
    st.code(sql_having_1, language="sql")
    if st.button("Run Query #4"):
        st.dataframe(run_query(sql_having_1))
    st.divider()
    
    # --- HAVING QUERY 2 ---
    st.subheader("5. Main Roles with Multiple Ingredients (≥2)")
    sql_having_2 = """SELECT Main_Role,COUNT(Ingredient_Id) AS Total_Ingrediente
FROM dbo.Ingredients
GROUP BY Main_Role
HAVING COUNT(Ingredient_Id)>=2;"""
    st.code(sql_having_2, language="sql")
    if st.button("Run Query #5"):
        st.dataframe(run_query(sql_having_2))

# =====================================================================
# TAB 2: PATIENT SKINCARE LOGS & DOCTOR APPROVALS
# =====================================================================
with tab_logs:
    st.header("Patient Usage & Reaction Form")
    st.write("Patients can log used products and describe skin reactions. Logs must be approved by a verified doctor.")
    
    with st.form("patient_log_form"):
        patient_name = st.text_input("Patient Name:", "Demo User")
        product_used = st.text_input("Product Used:", "e.g., Hydrating Serum")
        reaction_desc = st.text_area(
            "What happened to your skin after usage?", 
            "Describe any redness, hydration changes, or breakouts after applying the product."
        )
        submitted = st.form_submit_button("Submit for Dermatologist Review")
        
        if submitted and product_used and reaction_desc:
            # For POC: Displaying instant confirmation. 
            # In production, this runs: INSERT INTO UserLogs (PatientName, ProductUsed, Reaction, Status) VALUES (...)
            st.success("✅ Log submitted successfully! Current Status: **Pending Doctor Approval**.")
            
    st.subheader("✅ Doctor-Approved Patient Case Studies")
    # Mocking approved table display for the POC demo if a UserLogs table doesn't exist yet
    mock_logs = pd.DataFrame({
        "Patient": ["Alex M.", "Elena R."],
        "Product Used": ["Daily Hydrating Serum", "Active Retinol Cream"],
        "Skin Reaction": ["Reduced redness and improved texture after 7 days.", "Mild initial dryness, followed by clearer skin."],
        "Status": ["Approved by Dr. Popescu", "Approved by Dr. Ionescu"]
    })
    st.dataframe(mock_logs)
    st.divider()


    sql_clinics = "SELECT Clinic_Name AS Clinics, City FROM Clinics"
    st.subheader("🏥 Find a Verified Clinic Near You")
    st.write("Match your skincare log with a local dermatological clinic for physical consultation.")

    # 1. Fetch distinct cities dynamically from your Azure SQL table
    cities_df = run_query("SELECT DISTINCT City FROM dbo.Clinics WHERE City IS NOT NULL;")

    if not cities_df.empty:
        # Convert the dataframe column to a Python list and prepend an "All Cities" option
        city_list = ["All Cities"] + cities_df["City"].tolist()
        
        # 2. User Input: City Dropdown
        selected_city = st.selectbox("Select Your City to Filter Clinics:", city_list)
        
        # 3. Query the database based on the user's selection
        if selected_city == "All Cities":
            clinics_query = "SELECT Clinic_Name AS Clinics, City FROM dbo.Clinics;"
            clinics_df = run_query(clinics_query)
        else:
            # Using a parameterized query (?) to safely filter by the chosen city
            clinics_query = "SELECT Clinic_Name AS Clinics, City FROM dbo.Clinics WHERE City = ?;"
            clinics_df = run_query(clinics_query, (selected_city,))
            
        # 4. Display the filtered results
        if not clinics_df.empty:
            st.dataframe(clinics_df)
        else:
            st.info(f"No clinics found registered in {selected_city}.")
    else:
        st.warning("⚠️ Could not load cities. Please verify that 'dbo.Clinics' is the correct table name.")

# =====================================================================
# TAB 3: DATABASE EXPLORER
# =====================================================================
with tab_explorer:
    st.header("Quick Table Viewer")
    selected_table = st.selectbox("Select Table to View:", ["dbo.Products", "dbo.Brands", "dbo.Ingredients"])
    
    if st.button(f"Load {selected_table}"):
        df_table = run_query(f"SELECT * FROM {selected_table};")
        if not df_table.empty:
            st.dataframe(df_table)
        else:
            st.warning("Table is empty or could not be loaded.")