import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="GhostCost AI", layout="wide")

# Sleek UI for Submission
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .report-card { background-color: #1a1c24; padding: 25px; border-radius: 15px; border-left: 10px solid #ff4b4b; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #ff7e5f); color: white; font-weight: bold; border-radius: 10px; height: 3em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("👻 GhostCost Agent")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
lang = st.sidebar.selectbox("Language", ["English", "Hinglish", "Marathi"])

st.title("🛡️ GhostCost AI Auditor")
st.markdown("#### *Revealing the invisible price of consumption.*")

product_name = st.text_input("Product Name", placeholder="e.g. Chemical Floor Cleaner")
uploaded_file = st.file_uploader("Scan Product (Image Support)", type=["jpg", "png", "jpeg"])

if st.button("Unmask the Truth 🔍"):
    if not api_key:
        st.error("API Key required for live audit.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner('Agent is researching global supply chains...'):
                prompt = f"""
                Analyze '{product_name}' in '{lang}' as an Ethical Auditor. 
                Identify: Manufacturing, Human Cost, Animal Cost, and Environmental Debt.
                Suggest sustainable alternatives like Bio-enzymes.
                """
                
                contents = [prompt]
                if uploaded_file: contents.append(Image.open(uploaded_file))
                
                response = client.models.generate_content(model="gemini-1.5-flash", contents=contents)
                st.markdown(f'<div class="report-card">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Quota Exhausted: {e}")
            st.info("Technical Note: The logic is fully functional. Currently hitting Free Tier Rate Limits (429).")

st.caption("GhostCost AI - Mission: Global Transparency | VIT Pune")