import streamlit as st
from google import genai
from google.genai import types
from db import run_query

st.title("🤖 GlowMatch Dermo-Consultant AI")
st.write("Get AI-powered skincare recommendations grounded in our verified dermatological database.")
st.divider()

# 1. Initialize Gemini Client
# Assumes GEMINI_API_KEY is stored in .streamlit/secrets.toml
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ Gemini API Key not found in .streamlit/secrets.toml")
    st.stop()

# 2. Fetch Live Context from Azure SQL Database
@st.cache_data(ttl=600)
def get_db_context():
    products_df = run_query("SELECT Brand, Name, Type FROM dbo.Products;")
    ingredients_df = run_query("SELECT Ingredient_Name, Main_Role, Hydration_Level FROM dbo.Ingredients WHERE Is_Active_Ingredient=1;")
    return products_df, ingredients_df

products_df, ingredients_df = get_db_context()

# Create dropdown lists from DB data
product_list = products_df["Name"].tolist() if not products_df.empty else ["Serum Sample", "Moisturizer Sample"]
ingredient_summary = ingredients_df.to_dict(orient="records") if not ingredients_df.empty else "No live ingredient data."

# 3. Define AI Guardrails (System Prompt)
SYSTEM_INSTRUCTION = f"""
You are the GlowMatch AI Skincare Consultant. 
CRITICAL GUARDRAILS:
1. You are STRICTLY FORBIDDEN from giving medical advice, diagnosing skin conditions, or prescribing treatments.
2. If the user describes severe symptoms (bleeding, chronic pain, severe cystic acne, allergic reactions), immediately refuse medical assessment and advise them to schedule an consultation with a dermatologist from our verified clinic network.
3. Base your product compatibility analysis on the following active ingredients available in our database: {ingredient_summary}.
4. Keep your responses concise, empathetic, and scientifically grounded.
"""

# 4. Build User Interface
col1, col2 = st.columns(2)
with col1:
    user_skin_type = st.selectbox(
        "Select Your Skin Type:", 
        ["Normal", "Oily", "Dry", "Combination", "Sensitive / Acne-Prone"]
    )
with col2:
    selected_product = st.selectbox("Select a Product from our DB to Analyze:", product_list)

user_concerns = st.text_area(
    "Describe your skin goals or current concerns:", 
    "e.g., I want to add this serum to my routine, but my skin gets irritated easily by strong actives."
)

if st.button("✨ Analyze Compatibility", type="primary"):
    with st.spinner("Analyzing ingredient compatibility against your skin profile..."):
        # Construct dynamic prompt
        prompt = f"""
        User Profile:
        - Skin Type: {user_skin_type}
        - Interested Product: {selected_product}
        - User Notes/Concerns: {user_concerns}
        
        Please evaluate if this product is suitable for the user's skin type based on typical active ingredients, explain potential benefits or risks, and remind them to patch test.
        """
        
        try:
            # Call Gemini API with streaming for live presentation visual impact
            response = client.models.generate_content_stream(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3
                )
            )
            
            st.subheader("💡 Compatibility Analysis")
            # Streamlit's write_stream renders the generator in real-time
            st.write_stream(chunk.text for chunk in response if chunk.text)
            
        except Exception as e:
            st.error(f"AI Generation failed: {e}")