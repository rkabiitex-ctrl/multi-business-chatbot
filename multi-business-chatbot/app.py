

import streamlit as st
from openai import OpenAI

# 1. Setup the Web Page Layout & Tab Title
st.set_page_config(page_title="Universal AI Lead Booker", page_icon="🤖", layout="wide")

# 2. Inject Custom Elite CSS Styling for Premium Themes
st.markdown("""
    <style>
        .stApp { background-color: #0d0f12 !important; color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] { background-color: #13171e !important; border-right: 1px solid #222c3a; }
        h1, h2, h3, p, span, label { color: #f1f5f9 !important; }
        .stChatInput textarea { background-color: #1a202c !important; color: #ffffff !important; border: 1px solid #3a4659 !important; border-radius: 8px !important; }
        .gold-text { background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Title with Gold Styling
st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
st.write("Select a business category below to test how the AI adapts to capture customer leads via text or voice.")

# 3. Premium AI Packages in the Left Sidebar
st.sidebar.markdown('<h2 class="gold-text">💳 Premium AI Packages</h2>', unsafe_allow_html=True)
st.sidebar.write("Ready to deploy this AI Agent onto your actual business website?")
st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">🔹 Standard Package</p>', unsafe_allow_html=True)
st.sidebar.write("Ideal for Dentists, Gyms, Plumbers, and Auto Parts Stores.")
st.sidebar.link_button("Get Standard ($300/mo)", "PASTE_YOUR_300_PESAPAL_LINK")
st.sidebar.write("") 
st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">👑 Elite Luxury Package</p>', unsafe_allow_html=True)
st.sidebar.write("Custom-built for Yacht Charters, Exotic Rentals, & Estate Builders.")
st.sidebar.link_button("Get Elite ($500/mo)", "PASTE_YOUR_500_PESAPAL_LINK")
st.sidebar.divider()

# 4. Dropdown Menu for Global High-Ticket Industries & General AI Workspace
business_type = st.selectbox(
    "Choose an AI Agent Profile to Demo:",
    [
        "Global Dental Clinic Receptionist", 
        "Roofing & Solar Sales Closer", 
        "Fitness Gym Membership Agent", 
        "Emergency Plumbing Dispatcher",
        "Luxury Exotic Car Rental Agent",
        "Custom Luxury Home Builder Consultant",
        "Premium Yacht Charter Concierge",
        "Auto Parts & Accessories Specialist",
        "General ChatGPT AI Workspace"
    ]
)

# 5. Dynamically set the AI's Personality/Instructions based on selection
if business_type == "Global Dental Clinic Receptionist":
    system_instruction = "You are a friendly receptionist for a dental clinic. Answer basic dental questions. Your goal is to get their phone number/email to book a checkup."
    welcome_message = "Hello! Thanks for visiting our dental page today. Are you looking to book a routine cleaning?"
elif business_type == "Roofing & Solar Sales Closer":
    system_instruction = "You are a sales assistant for a roofing contractor. Your goal is to get the customer's address and phone number to schedule a free roof inspection."
    welcome_message = "Hi there! Welcome to our roofing page. Are you looking for a free estimate on a repair or replacement?"
elif business_type == "Fitness Gym Membership Agent":
    system_instruction = "You are an energetic assistant for a gym. Your goal is to get the customer's email address to sign them up for a free 3-day workout pass."
    welcome_message = "Let's go! Welcome to the gym portal. Ready to smash your fitness goals?"
elif business_type == "Emergency Plumbing Dispatcher":
    system_instruction = "You are an urgent customer agent for a plumbing service. Your goal is to get their phone number and a description of their issue immediately."
    welcome_message = "Express Plumbing here! Do you have an active leak, a clogged drain, or a plumbing emergency right now?"
elif business_type == "Luxury Exotic Car Rental Agent":
    system_instruction = "You are an elite concierge for an exotic car rental agency. Your goal is to find out which supercar they want, the dates, and get their contact info."
    welcome_message = "Welcome to our luxury fleet concierge. Are you looking to secure an exotic rental for an upcoming trip?"
elif business_type == "Custom Luxury Home Builder Consultant":
    system_instruction = "You are an architectural design consultant for a luxury home builder. Your goal is to discover their budget, location, and get their phone number."
    welcome_message = "Welcome to our custom estate design portal. Are you looking to build on your own lot?"
elif business_type == "Premium Yacht Charter Concierge":
    system_instruction = "You are a polished concierge for a luxury yacht charter. Your goal is to find out the destination, party size, travel dates, and capture their contact info."
    welcome_message = "Welcome to our premium charter concierge. Are you planning an upcoming private excursion?"
elif business_type == "Auto Parts & Accessories Specialist":
    system_instruction = "You are an expert support agent for an auto parts store. Your goal is to find out their vehicle year, make, model, and capture their phone number."
    welcome_message = "Auto parts specialist here! What vehicle year, make, and model are we working on today?"
elif business_type == "General ChatGPT AI Workspace":
    system_instruction = "You are ChatGPT, a highly helpful, intelligent AI assistant. Answer any creative, school, or code question directly. Do NOT ask for phone numbers or bookings."
    welcome_message = "Welcome to your General ChatGPT AI Workspace! 🚀 Ask me anything, or speak a voice command!"

st.divider()

# Track active business type to force refresh memory when dropdown switches
if "current_business" not in st.session_state:
    st.session_state.current_business = business_type

if st.session_state.current_business != business_type:
    st.session_state.current_business = business_type
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

# 6. Initialize Chat History in Streamlit Memory
if "messages" not in st.session_state or st.sidebar.button("Reset Chat"):
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "audio" in msg:
            st.audio(msg["audio"], format="audio/mp3")

# 7. Voice Input Control Module
st.markdown('<p style="color: #bf953f; font-weight: bold;">🎙️ Voice Command Feature</p>', unsafe_allow_html=True)
voice_input = st.audio_input("Tap the microphone below to speak your request:")

user_message = None

if voice_input is not None:
    try:
        client = OpenAI()
        with st.spinner("Analyzing voice command..."):
            transcription = client.audio.transcriptions.create(model="whisper-1", file=voice_input)
            user_message = transcription.text
    except Exception as e:
        st.error(f"Voice Transcription Error: {e}")

chat_input = st.chat_input("Or type your message here manually...")
if chat_input:
    user_message = chat_input

# 8. Processing Engine (Handles Text & Audio Generation)
if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.rerun()

if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Processing response..."):
            try:
                client = OpenAI()
                api_messages = [{"role": "system", "content": system_instruction}]
                for m in st.session_state.messages:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages)
                ai_text = response.choices.message.content
                st.write(ai_text)
                
                audio_response = client.audio.speech.create(model="tts-1", voice="alloy", input=ai_text)
                audio_bytes = audio_response.content
                st.audio(audio_bytes, format="audio/mp3")
                
                st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": audio_bytes})
                st.rerun()
            except Exception as e:
                st.error(f"System Error: {e}. Check your OpenAI balance or key config.")

      


                
            
                   
              
