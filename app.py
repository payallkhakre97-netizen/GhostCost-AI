import streamlit as st
from google import genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="GhostCost AI | Global Auditor", layout="wide")

# 2. Sidebar
st.sidebar.title("👻 GhostCost Agent")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
lang = st.sidebar.selectbox("Preferred Language", ["English", "Hindi", "Marathi", "Hinglish"])

# 3. Main Interface
st.title("🛡️ GhostCost AI")
product_name = st.text_input("Product Name", placeholder="e.g. Leather Boots")
uploaded_file = st.file_uploader("Scan Product (Image)", type=["jpg", "jpeg", "png"])
st.markdown("""
    <style>
    .stInfo { background-color: #1e1e1e; border-left: 8px solid #FF4B2B; border-radius: 10px; color: white; font-size: 18px; }
    h1, h2, h3 { color: #FF4B2B !important; }
    .stButton>button { background: linear-gradient(45deg, #FF4B2B, #FF416C); color: white; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if st.button("Unmask the Truth 🔍"):
    if not api_key:
        st.error("Bhai, sidebar mein API Key toh daalo!")
    elif not product_name and not uploaded_file:
        st.warning("Please provide a product name or an image.")
    else:
        try:
            # Stable SDK Initialization
            client = genai.Client(api_key=api_key)
            model_id = "gemini-2.5-flash" 
            
            with st.spinner('Agent is reasoning...'):
                system_prompt = f"Act as 'GhostCost' Ethical Auditor. Analyze {product_name} in {lang}. Identify: 1. Manufacturing 2. Human Cost 3. Animal Cost 4. Environmental Debt. Give a Ghost Score (1-10)."
                system_prompt = f"""
Act as 'GhostCost' Ethical Auditor. Analyze {product_name} in {lang}. 

FORMATTING: Use bold headings and bullet points.
Identify:
1. **MANUFACTURING**: (Highlight 2-3 key points)
2. **HUMAN COST**: (Impact on labor/communities)
3. **ANIMAL COST**: (Cruelty level)
4. **ENVIRONMENTAL DEBT**: (Pollution/waste)
5. **GHOST SCORE**: (Give a percentage % of environmental impact)
6. **🌱 SUSTAINABLE ALTERNATIVES**: (Suggest organic/eco-friendly products like Bio-enzymes)
"""
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = client.models.generate_content(model=model_id, contents=[system_prompt, img])
                else:
                    response = client.models.generate_content(model=model_id, contents=[system_prompt])
                
                st.subheader("📊 Truth Report")
                st.info(response.text)
                
        except Exception as e:
            st.error(f"Logic Error: {e}")
# --- REAL INTERACTIVE CHATBOT SECTION ---
st.divider()
st.subheader("💬 Chat with GhostCost AI")

# 1. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Input
if prompt := st.chat_input("Ask me about the ethical impact of this product..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Real AI Response
    try:
        client = genai.Client(api_key=api_key)
        # We use a simple prompt to keep it conversational
        chat_response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Context: Analyzing {product_name}. User says: {prompt}. Reply as the GhostCost Ethical Auditor in {lang}."
        )
        
        full_response = chat_response.text
        
        # Add AI response to history
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error("Please enter a valid API Key in the sidebar to chat!")
st.caption("GhostCost AI - VIT Pune")
