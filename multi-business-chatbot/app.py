import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Elite AI Workspace", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0d0f12 !important; color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] { background-color: #13171e !important; border-right: 1px solid #222c3a; }
        h1, h2, h3, p, span, label { color: #f1f5f9 !important; }
        .stChatInput textarea { background-color: #1a202c !important; color: #ffffff !important; border: 1px solid #3a4659 !important; border-radius: 8px !important; }
        .stTextArea textarea, .stTextInput input { color: #1e293b !important; font-weight: 500 !important; }
        .gold-text { background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
        .package-header { color: #bf953f !important; font-weight: bold !important; font-size: 18px !important; margin-bottom: 2px !important; }
        .package-desc { color: #e2e8f0 !important; font-size: 14px !important; margin-bottom: 10px !important; }
    </style>
""", unsafe_allow_html=True)

if "local_case_vault_text" not in st.session_state: st.session_state.local_case_vault_text = ""
if "local_case_vault_brief" not in st.session_state: st.session_state.local_case_vault_brief = ""

st.sidebar.markdown('<h2 class="gold-text">🧭 Workspace Navigation</h2>', unsafe_allow_html=True)
app_mode = st.sidebar.radio("Go to Page:", ["🤖 AI Lead Booking Agent", "⚖️ Judicial Case Analyzer"])
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

if app_mode == "🤖 AI Lead Booking Agent":
    st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
    st.write("Select a business category below to test how the AI adapts to capture customer leads via text or voice.")
    business_type = st.selectbox("Choose an AI Agent Profile to Demo:", ["Global Dental Clinic Receptionist", "Elite Med-Spa & Cosmetics Concierge", "Roofing & Solar Sales Closer", "Fitness Gym Membership Agent", "Emergency Plumbing Dispatcher", "Luxury Exotic Car Rental Agent", "Custom Luxury Home Builder Consultant", "Premium Yacht Charter Concierge", "Auto Parts & Accessories Specialist", "General ChatGPT AI Workspace"], key="master_business_selector_v3")

    if business_type == "Global Dental Clinic Receptionist":
        sys_inst, welcome_msg = "You are a receptionist for a dental clinic. Get their phone to book.", "Hello! Thanks for visiting our dental page today. Looking to book a cleaning?"
    elif business_type == "Elite Med-Spa & Cosmetics Concierge":
        sys_inst, welcome_msg = "You are an elite booking concierge for a medical spa. Ask for phone or WhatsApp to book.", "Welcome to our premier aesthetics concierge. ✨ Looking to explore skin treatments today?"
    elif business_type == "Roofing & Solar Sales Closer":
        sys_inst, welcome_msg = "You are a roofing sales assistant. Get address and phone for inspection.", "Hi there! Welcome to our roofing page. Need a free estimate?"
    elif business_type == "Fitness Gym Membership Agent":
        sys_inst, welcome_msg = "You are a gym assistant. Get email for workout pass.", "Let's go! Welcome to the gym portal. Ready to smash your fitness goals?"
    elif business_type == "Emergency Plumbing Dispatcher":
        sys_inst, welcome_msg = "You are a plumbing dispatcher. Get phone and emergency details.", "Express Plumbing here! Do you have an active leak or emergency right now?"
    elif business_type == "Luxury Exotic Car Rental Agent":
        sys_inst, welcome_msg = "You are a supercar concierge. Find vehicle, dates, and contact info.", "Welcome to our luxury fleet concierge. Looking to secure an exotic rental?"
    elif business_type == "Custom Luxury Home Builder Consultant":
        sys_inst, welcome_msg = "You are a design consultant. Discover budget, location, and get phone.", "Welcome to our custom estate design portal. Looking to build on your own lot?"
    elif business_type == "Premium Yacht Charter Concierge":
        sys_inst, welcome_msg = "You are a yacht concierge. Get destination, party size, dates, and contact.", "Welcome to our premium charter concierge. Planning a private excursion?"
    elif business_type == "Auto Parts & Accessories Specialist":
        sys_inst, welcome_msg = "You are a parts agent. Find vehicle details and get phone number.", "Auto parts specialist here! What vehicle year, make, and model are we working on today?"
    elif business_type == "General ChatGPT AI Workspace":
        sys_inst, welcome_msg = "You are ChatGPT, a helpful assistant. Provide value.", "Welcome to your General ChatGPT AI Workspace! 🚀 Ask me anything!"

    if "active_profile_selection" not in st.session_state: st.session_state.active_profile_selection = business_type
    if st.session_state.active_profile_selection != business_type:
        st.session_state.active_profile_selection = business_type
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

    if "messages" not in st.session_state or st.sidebar.button("Reset Chat", key="reset_chat_agent_v3"):
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    chat_input = st.chat_input("Or type your message here manually...")
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        try:
            client = OpenAI()
            api_messages = [{"role": "system", "content": sys_inst}]
            for m in st.session_state.messages:
                if m["role"] in ["user", "assistant"]: api_messages.append({"role": m["role"], "content": str(m["content"])})
            response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages)
            ai_text = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            st.rerun()
        except Exception as e: st.error(f"System Error: {e}")

elif app_mode == "⚖️ Judicial Case Analyzer":
    st.markdown('<h1 class="gold-text">⚖️ Legal & Judicial Case Analyzer</h1>', unsafe_allow_html=True)
    st.write("Paste legal case texts below. Your text and briefs remain locked securely in runtime memory arrays.")
    st.divider()
    
    case_text = st.text_area("Paste Case Legal Text Here:", value=st.session_state.local_case_vault_text, height=250)
    if case_text != st.session_state.local_case_vault_text:
        st.session_state.local_case_vault_text = case_text
        
    col1, col2 = st.columns(2)
    with col1: run_analysis = st.button("🔥 Run AI Judicial Analysis", key="judicial_analysis_btn")
    with col2:
        if st.button("🗑️ Clear Workspace Memory", key="clear_workspace_btn"):
            st.session_state.local_case_vault_text = ""
            st.session_state.local_case_vault_brief = ""
            st.rerun()
            
    if run_analysis:
        if case_text:
            with st.spinner("Compiling judicial brief..."):
                try:
                    client = OpenAI()
                    legal_instruction = "You are senior judicial counsel. Break into: 1. CORE FACTS, 2. CLAIMS, 3. LAWS, 4. RECOMMENDATION."
                    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": legal_instruction}, {"role": "user", "content": case_text}])
                    st.session_state.local_case_vault_brief = response.choices[0].message.content
                    st.rerun()
                except Exception as e: st.error(f"Analysis Error: {e}")
        else: st.warning("Please paste some legal text first!")
        
    if st.session_state.local_case_vault_brief:
        st.success("Analysis Securely Loaded from Workspace Memory!")
        st.markdown("### 🏛️ Official AI Case Evaluation Brief")
        st.info(st.session_state.local_case_vault_brief)
