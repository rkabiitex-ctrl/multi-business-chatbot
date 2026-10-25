import streamlit as st
from openai import OpenAI
import re
import json
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & ENTERPRISE THEME
# ==========================================
st.set_page_config(page_title="Elite AI Workspace", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0d0f12 !important; color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] { background-color: #13171e !important; border-right: 1px solid #222c3a; }
        h1, h2, h3, p, span, label { color: #f1f5f9 !important; }
        .stChatInput textarea { background-color: #1a202c !important; color: #ffffff !important; border: 1px solid #3a4659 !important; border-radius: 8px !important; }
        .stTextArea textarea, .stTextInput input { color: #ffffff !important; background-color: #1e293b !important; font-weight: 500 !important; }
        .gold-text { background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
        .package-header { color: #bf953f !important; font-weight: bold !important; font-size: 18px !important; margin-bottom: 2px !important; }
        .package-desc { color: #e2e8f0 !important; font-size: 14px !important; margin-bottom: 10px !important; }
        
        .stButton>button, .stLinkButton>a {
            color: #ffffff !important;
            font-weight: bold !important;
            text-decoration: none !important;
            background-color: #1c2431 !important;
            border: 1px solid #bf953f !important;
        }
        .stButton>button:hover, .stLinkButton>a:hover {
            background-color: #bf953f !important;
            color: #0d0f12 !important;
        }
    </style>
""", unsafe_allow_html=True)

if "local_case_vault_text" not in st.session_state: st.session_state.local_case_vault_text = ""
if "local_case_vault_brief" not in st.session_state: st.session_state.local_case_vault_brief = ""
if "lead_extraction_status" not in st.session_state: st.session_state.lead_extraction_status = "unverified"

# ==========================================
# 2. RUNTIME LEAD CAPTURE VALIDATION ENGINES
# ==========================================
def extract_and_log_lead(user_text, business_profile):
    phone_match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}\text[-.\s]?\d{4}|\b\d{10}\b', user_text)
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', user_text)
    
    extracted_data = {}
    if phone_match: extracted_data["phone"] = phone_match.group(0)
    if email_match: extracted_data["email"] = email_match.group(0)
    
    if extracted_data:
        st.session_state.lead_extraction_status = "VERIFIED"
        print(f"🔥 HOT LEAD LOGGED [{business_profile}]: {json.dumps(extracted_data)} at {datetime.now()}")
        return True
    return False

# ==========================================
# 3. SIDEBAR NAVIGATION & PACKAGES
# ==========================================
st.sidebar.markdown('<h2 class="gold-text">🧭 Workspace Navigation</h2>', unsafe_allow_html=True)
app_mode = st.sidebar.radio("Go to Page:", ["🧠 AI Lead Booking Agent", "⚖️ Judicial Case Analyzer"])
st.sidebar.divider()

st.sidebar.markdown('<h3 class="gold-text">💳 Premium AI Packages</h3>', unsafe_allow_html=True)
st.sidebar.write("Ready to deploy this system onto your real organization website?")
st.sidebar.divider()

st.sidebar.markdown('<p class="package-header">🔹 Standard Package</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="package-desc">Ideal for Businesses, Clinics, and Stores.</p>', unsafe_allow_html=True)
st.sidebar.link_button("✨ Get Standard ($300/mo)", "PASTE_YOUR_300_PESAPAL_LINK")

st.sidebar.write("")
st.sidebar.markdown('<p class="package-header">👑 Elite Luxury Package</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="package-desc">Custom-built for Courts, Law Firms, Yacht Charters, & Developers.</p>', unsafe_allow_html=True)
st.sidebar.link_button("👑 Get Elite ($500/mo)", "PASTE_YOUR_500_PESAPAL_LINK")
st.sidebar.divider()

# ==========================================
# 4. DATA MATRIX CONFIGURATIONS
# ==========================================
PROFILE_RULES = {
    "Global Dental Clinic Receptionist": ("You are a receptionist for a dental clinic. Systematically ask for their phone number or contact info to secure an urgent treatment slot tomorrow.", "Hello! Thanks for visiting our dental page today. Looking to book an urgent cleaning or checkup tomorrow?"),
    "Elite Med-Spa & Cosmetics Concierge": ("You are an elite booking concierge for a medical spa. Secure their phone number or WhatsApp to reserve aesthetics services.", "Welcome to our premier aesthetics concierge. ✨ Looking to explore skin treatments today?"),
    "Roofing & Solar Sales Closer": ("You are an expert roofing sales assistant. Convince the customer an inspector needs to visit, then gather their address and phone number.", "Hi there! Welcome to our roofing services portal. Experiencing leaks or looking for a free architectural estimate?"),
    "Fitness Gym Membership Agent": ("You are a high-energy gym assistant. Get their email or phone number to drop a free day pass to their mobile device.", "Let's go! Welcome to the fitness hub. Ready to crush your wellness goals? What's your email to get your free pass?"),
    "Emergency Plumbing Dispatcher": ("You are an emergency plumbing dispatcher. Instantly secure their primary contact number to send out an on-call team.", "Express Plumbing here! Do you have an active leak, burst pipe, or emergency right now?"),
    "Luxury Exotic Car Rental Agent": ("You are a supercar rental coordinator. Find out their target vehicle class and secure contact info to send verification requirements.", "Welcome to our luxury fleet concierge. Looking to secure an exotic rental confirmation for tomorrow?"),
    "Custom Luxury Home Builder Consultant": ("You are an upscale design consultant. Uncover their budget tier, geographical market, and secure a callback line.", "Welcome to our custom estate design portal. Looking to build or remodel a luxury property on your lot?"),
    "Premium Yacht Charter Concierge": ("You are a private maritime cruise concierge. Get destination layout details, guest numbers, dates, and clear contact numbers.", "Welcome to our premium charter concierge. Planning a private coastal excursion or yacht gathering?"),
    "Auto Parts & Accessories Specialist": ("You are a parts desk specialist. Secure vehicle specs (year, make, model) along with phone numbers for fulfillment tracking.", "Auto parts specialist here! What vehicle year, make, and model are we sourcing components for today?"),
    "General ChatGPT AI Workspace": ("You are ChatGPT, a highly helpful assistant. Provide extreme value.", "Welcome to your General ChatGPT AI Workspace! 🚀 Ask me anything!")
}

# ==========================================
# 5. RENDER CHANNELS
# ==========================================
if app_mode == "🧠 AI Lead Booking Agent":
    st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
    st.write("Select a business category below to test how the AI adapts to capture customer leads via text or voice.")
    
    business_type = st.selectbox(
        "Choose an AI Agent Profile to Demo:", 
        list(PROFILE_RULES.keys()),
        key="master_business_selector_v3"
    )

    sys_inst, welcome_msg = PROFILE_RULES[business_type]

    if "active_profile_selection" not in st.session_state: 
        st.session_state.active_profile_selection = business_type
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

    if st.session_state.active_profile_selection != business_type:
        st.session_state.active_profile_selection = business_type
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
        st.session_state.lead_extraction_status = "unverified"

    if "messages" not in st.session_state or st.sidebar.button("Reset Chat", key="reset_chat_agent_v3"):
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
        st.session_state.lead_extraction_status = "unverified"

    if st.session_state.lead_extraction_status == "VERIFIED":
        st.success("🚨 TARGET CONTACT INFO SUCCESSFULLY CAPTURED & EXECUTED ON THE BACKEND")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    chat_input = st.chat_input("Or type your message here manually...")
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        extract_and_log_lead(chat_input, business_type)
        
        try:
            client = OpenAI()
            api_messages = [{"role": "system", "content": sys_inst}]
            for m in st.session_state.messages:
                if m["role"] in ["user", "assistant"]: 
                    api_messages.append({"role": m["role"], "content": str(m["content"])})
            
            response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages)
            ai_text = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            st.rerun()
        except Exception as e: 
            st.error(f"System Error: {e}")

elif app_mode == "⚖️ Judicial Case Analyzer":
    st.markdown('<h1 class="gold-text">⚖️ Legal & Judicial Case Analyzer</h1>', unsafe_allow_html=True)
    st.write("Paste legal case texts below. Your text and briefs remain locked securely in runtime memory arrays.")
    st.divider()
    
    case_text = st.text_area("Paste Case Legal Text Here:", value=st.session_state.local_case_vault_text, height=250)
    if case_text != st.session_state.local_case_vault_text:
