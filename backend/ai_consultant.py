from google import genai
from google.genai import types
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = """
You are the GlowMatch AI Dermo-Consultant. 
RULES:
1. You MUST NOT provide medical advice, diagnoses, or prescriptions.
2. Analyze skincare product compatibility based strictly on ingredient lists and user skin type.
3. If the user mentions pain, bleeding, severe acne, or allergic reactions, advise them to see a medical professional and recommend doctors from the provided database list only.
"""

def get_skin_analysis_stream(skin_type, product_name, ingredients, available_doctors):
    prompt = f"""
    User Skin Type: {skin_type}
    Selected Product: {product_name}
    Product Ingredients: {ingredients}
    Available Doctors in DB: {available_doctors}
    
    Provide a brief compatibility analysis and usage recommendation.
    """
    
    response = client.models.generate_content_stream(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.3
        )
    )
    return response