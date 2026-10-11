


import streamlit as st
from openai import OpenAI

# 1. Setup the Web Page Layout & Tab Title
st.set_page_config(page_title="Elite AI Workspace", page_icon="🤖", layout="wide")

# 2. Inject Custom Elite CSS Styling for Premium Themes
st.markdown("""
    <style>
        .stApp { background-color: #0d0f12 !important; color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] { background-color: #13171e !important; border-right: 1px solid #222c3a; }
        h1, h2, h3, p, span, label { color: #f1f5f9 !important; }
        .stChatInput textarea { background-color: #1a202c !important; color: #ffffff !important; border: 1px solid #3a4659 !important; border-radius: 8px !important; }
        .stTextArea textarea, .stTextInput input { color: #1e293b !important; font-weight: 500 !important; }
        .gold-text { background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar App Navigation Control Hub
st.sidebar.markdown('<h2 class="gold-text">🧭 Workspace Navigation</h2>', unsafe_allow_html=True)
app_mode = st.sidebar.radio("Go to Page:", ["🤖 AI Lead Booking Agent", "⚖️ Judicial Case Analyzer"])
st.sidebar.divider()

# 4. Premium AI Packages in the Left Sidebar
st.sidebar.markdown('<h3 class="gold-text">💳 Premium AI Packages</h3>', unsafe_allow_html=True)
st.sidebar.write("Ready to deploy this system onto your real organization website?")
st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">🔹 Standard Package</p>', unsafe_allow_html=True)
st.sidebar.write("Ideal for Businesses, Clinics, and Stores.")
st.sidebar.link_button("Get Standard ($300/mo)", "PASTE_YOUR_300_PESAPAL_LINK")
st.sidebar.write("") 
st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">👑 Elite Judicial & Luxury Package</p>', unsafe_allow_html=True)
st.sidebar.write("Custom-built for Courts, Law Firms, Yacht Charters, & Developers.")
st.sidebar.link_button("Get Elite ($500/mo)", "PASTE_YOUR_500_PESAPAL_LINK")
st.sidebar.divider()

# ==========================================
# PAGE 1: THE BUSINESS & LEAD BOOKING AGENT
# ==========================================
if app_mode == "🤖 AI Lead Booking Agent":
    st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
    st.write("Select a business category below to test how the AI adapts to capture customer leads via text or voice.")

    business_type = st.selectbox(
        "Choose an AI Agent Profile to Demo:",
        [
            "Global Dental Clinic Receptionist", "Elite Med-Spa & Cosmetics Concierge", 
            "Roofing & Solar Sales Closer", "Fitness Gym Membership Agent", 
            "Emergency Plumbing Dispatcher", "Luxury Exotic Car Rental Agent", 
            "Custom Luxury Home Builder Consultant", "Premium Yacht Charter Concierge", 
            "Auto Parts & Accessories Specialist", "General ChatGPT AI Workspace"
        ]
    )

    if business_type == "Global Dental Clinic Receptionist":
        system_instruction = "You are a receptionist for a dental clinic. Get their phone/email to book a checkup."
        welcome_message = "Hello! Thanks for visiting our dental page today. Looking to book a routine cleaning?"
    elif business_type == "Elite Med-Spa & Cosmetics Concierge":
        system_instruction = "You are an elite booking concierge for a premium medical spa. Answer questions about Botox, fillers, and skincare. Get their phone number or WhatsApp to book an aesthetics consultation."
        welcome_message = "Welcome to our premier aesthetics concierge. ✨ Looking to explore skin treatments or book a cosmetic consultation today?"
    elif business_type == "Roofing & Solar Sales Closer":
        system_instruction = "You are a roofing sales assistant. Get their address and phone number for a free inspection."
        welcome_message = "Hi there! Welcome to our roofing page. Need a free estimate on a repair or replacement?"
    elif business_type == "Fitness Gym Membership Agent":
        system_instruction = "You are an energetic gym assistant. Get their email for a free 3-day workout pass."
        welcome_message = "Let's go! Welcome to the gym portal. Ready to smash your fitness goals?"
    elif business_type == "Emergency Plumbing Dispatcher":
        system_instruction = "You are an urgent plumbing dispatcher. Get their phone number and emergency description immediately."
        welcome_message = "Express Plumbing here! Do you have an active leak or emergency right now?"
    elif business_type == "Luxury Exotic Car Rental Agent":
        system_instruction = "You are an elite supercar concierge. Find out which car they want, dates, and get their contact info."
        welcome_message = "Welcome to our luxury fleet concierge. Looking to secure an exotic rental for an upcoming trip?"
    elif business_type == "Custom Luxury Home Builder Consultant":
        system_instruction = "You are a luxury estate design consultant. Discover their budget, location, and get their phone number."
        welcome_message = "Welcome to our custom estate design portal. Are you looking to build on your own lot?"
    elif business_type == "Premium Yacht Charter Concierge":
        system_instruction = "You are a polished yacht concierge. Get destination, party size, travel dates, and contact info."
        welcome_message = "Welcome to our premium charter concierge. Planning an upcoming private excursion?"
    elif business_type == "Auto Parts & Accessories Specialist":
        system_instruction = "You are an expert auto parts agent. Find out vehicle year, make, model, and get their phone number."
        welcome_message = "Auto parts specialist here! What vehicle year, make, and model are we working on today?"
    elif business_type == "General ChatGPT AI Workspace":
        system_instruction = "You are ChatGPT, a highly helpful, intelligent AI assistant. Provide pure value. Do NOT ask for booking details."
        welcome_message = "Welcome to your General ChatGPT AI Workspace! 🚀 Ask me anything, or speak a voice command!"

    st.divider()

    if "current_business" not in st.session_state: st.session_state.current_business = business_type
    if st.session_state.current_business != business_type:
        st.session_state.current_business = business_type
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

    if "messages" not in st.session_state or st.sidebar.button("Reset Chat"):
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "audio" in msg: st.audio(msg["audio"], format="audio/mp3")

    st.markdown('<p style="color: #bf953f; font-weight: bold;">🎙️ Voice Command Feature</p>', unsafe_allow_html=True)
    voice_input = st.audio_input("Tap the microphone below to speak your request:")

    user_message = None
    if voice_input is not None:
        try:
            client = OpenAI()
            with st.spinner("Analyzing voice command..."):
                transcription = client.audio.transcriptions.create(model="whisper-1", file=voice_input)
                user_message = transcription.text
        except Exception as e: st.error(f"Voice Error: {e}")

    chat_input = st.chat_input("Or type your message here manually...")
    if chat_input: user_message = chat_input

    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.rerun()

    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Processing response..."):
                try:
                    client = OpenAI()
                    api_messages = [{"role": "system", "content": system_instruction}]
                    for m in st.session_state.messages: api_messages.append({"role": m["role"], "content": m["content"]})
                    response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages)
                    ai_text = response.choices.message.content
                    st.write(ai_text)
                    audio_response = client.audio.speech.create(model="tts-1", voice="alloy", input=ai_text)
                    st.audio(audio_response.content, format="audio/mp3")
                    st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": audio_response.content})
                    st.rerun()
                except Exception as e: st.error(f"System Error: {e}. Check your OpenAI balance.")

# ==========================================
# PAGE 2: THE JUDICIAL CASE ANALYZER
# ==========================================
elif app_mode == "⚖️ Judicial Case Analyzer":
    st.markdown('<h1 class="gold-text">⚖️ Legal & Judicial Case Analyzer</h1>', unsafe_allow_html=True)
    st.write("Paste legal case texts below to instantly generate summaries and judicial breakdowns.")
    st.divider()
    case_text = st.text_area("Paste Case Legal Text Here:", height=250)
    if st.button("🔥 Run AI Judicial Analysis"):
        if case_text:
            with st.spinner("Compiling judicial brief..."):
                try:
                    client = OpenAI()
                    legal_instruction = "You are a senior judicial counsel. Analyze the text. Break it down into: 1. CORE CASE FACTS, 2. CLAIMS & ARGUMENTS, 3. APPLICABLE LAWS, and 4. SUGGESTED JUDICIAL RECOMMENDATION."
                    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": legal_instruction}, {"role": "user", "content": case_text}])
