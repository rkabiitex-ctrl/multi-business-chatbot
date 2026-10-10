


import streamlit as st
from openai import OpenAI

# 1. Setup the Web Page Layout & Tab Title
st.set_page_config(page_title="Universal AI Lead Booker", page_icon="🤖", layout="wide")

# 2. Inject Custom Elite CSS Styling for Premium Themes
st.markdown("""
    <style>
        /* Main page background */
        .stApp {
            background-color: #0d0f12 !important;
            color: #e2e8f0 !important;
        }
        
        /* Left Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #13171e !important;
            border-right: 1px solid #222c3a;
        }
        
        /* Global font color fixes */
        h1, h2, h3, p, span, label {
            color: #f1f5f9 !important;
        }
        
        /* Styling the Chat Input area */
        .stChatInput textarea {
            background-color: #1a202c !important;
            color: #ffffff !important;
            border: 1px solid #3a4659 !important;
            border-radius: 8px !important;
        }
        
        /* Custom Styling for the Luxury Headers */
        .gold-text {
            background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Title with Gold Styling
st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
st.write("Select a business category below to test how the AI adapts to capture customer leads.")

# 3. Premium AI Packages in the Left Sidebar
st.sidebar.markdown('<h2 class="gold-text">💳 Premium AI Packages</h2>', unsafe_allow_html=True)
st.sidebar.write("Ready to deploy this AI Agent onto your actual business website?")

st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">🔹 Standard Package</p>', unsafe_html=True)
st.sidebar.write("Ideal for Dentists, Gyms, Plumbers, and Auto Parts Stores.")
st.sidebar.link_button("Get Standard ($300/mo)", "PASTE_YOUR_300_FLUTTERWAVE_LINK")

st.sidebar.write("") # Extra spacing

st.sidebar.markdown('<p style="color: #bf953f !important; font-weight: bold;">👑 Elite Luxury Package</p>', unsafe_html=True)
st.sidebar.write("Custom-built for Yacht Charters, Exotic Rentals, & Estate Builders.")
st.sidebar.link_button("Get Elite ($500/mo)", "PASTE_YOUR_500_FLUTTERWAVE_LINK")

st.sidebar.divider()

# 4. Dropdown Menu for Global High-Ticket Industries
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
        "Auto Parts & Accessories Specialist"
    ]
)

# 5. Dynamically set the AI's Personality/Instructions based on selection
if business_type == "Global Dental Clinic Receptionist":
    system_instruction = "You are a friendly, professional receptionist for a high-end dental clinic. Answer basic dental questions politely. Your primary goal is to get the customer's phone number or email to book them a dental checkup."
    welcome_message = "Hello! Thanks for visiting our clinic page today. Are you looking to book a routine cleaning, or do you have a quick dental question?"

elif business_type == "Roofing & Solar Sales Closer":
    system_instruction = "You are a professional sales assistant for a roofing and solar contracting company. Be confident and helpful. Your primary goal is to get the customer's address and phone number to schedule a free property inspection."
    welcome_message = "Hi there! Welcome to our project page. Are you looking for a free estimate on a roof repair, solar installation, or a full replacement?"

elif business_type == "Fitness Gym Membership Agent":
    system_instruction = "You are an energetic, motivational assistant for a fitness gym. Be hyped up and encouraging. Your primary goal is to get the customer's email address to sign them up for a free 3-day workout pass."
    welcome_message = "Let's go! Welcome to the gym portal. Ready to smash your fitness goals? Ask me anything about our membership plans, pricing, or classes!"

elif business_type == "Emergency Plumbing Dispatcher":
    system_instruction = "You are an urgent, reliable customer agent for an emergency plumbing service. Be understanding and quick. Your primary goal is to get their phone number and a description of their issue so a technician can call them back immediately."
    welcome_message = "Emergency dispatch line here! Do you have an active leak, a clogged drain, or a plumbing emergency right now?"

elif business_type == "Luxury Exotic Car Rental Agent":
    system_instruction = "You are a high-end, elite concierge for a luxury exotic car rental agency managing supercars (Lamborghinis, Ferraris, Rolls-Royces). Be exclusive, polite, and efficient. Your primary goal is to find out which car they want, the dates they need it, and get their phone number and email to check fleet availability."
    welcome_message = "Welcome to our luxury fleet concierge. Are you looking to secure an exotic rental for an upcoming trip, or checking availability on a specific supercar today?"

elif business_type == "Custom Luxury Home Builder Consultant":
    system_instruction = "You are a sophisticated architectural design consultant for a high-end custom luxury home building company. Be articulate, professional, and knowledgeable about upscale building materials. Your primary goal is to discover their budget range, intended build location, and get their contact info to schedule a design consultation with the chief architect."
    welcome_message = "Welcome to our custom estate design portal. Are you looking to build on your own lot, or exploring architectural floor plans for a new luxury build?"

elif business_type == "Premium Yacht Charter Concierge":
    system_instruction = "You are an elite, polished concierge for a luxury yacht charter and rental brokerage. Speak with absolute refinement. Your primary goal is to find out the destination (e.g., Miami, Monaco, Bahamas), the size of their guest party, the date of travel, and capture their phone number/email to send a custom charter quote."
    welcome_message = "Welcome to our premium charter concierge. Are you planning an upcoming private excursion, corporate event, or looking for specific yacht availabilities?"

elif business_type == "Auto Parts & Accessories Specialist":
    system_instruction = "You are an expert, helpful customer support representative for a high-volume car auto parts and performance accessories store. Be precise and technically knowledgeable. Your primary goal is to find out their vehicle's year, make, and model, determine the specific part or performance upgrade they are searching for, and capture their phone number or email to check local inventory availability immediately."
    welcome_message = "Auto parts specialist here! What vehicle year, make, and model are we working on today, and what specific parts or upgrades are you trying to find?"

st.divider()

# 6. Initialize Chat History in Streamlit Memory
if "messages" not in st.session_state or st.sidebar.button("Reset Chat"):
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

# Display the ongoing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. Handle User Chat Input
if user_input := st.chat_input("Type your message here..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Responding..."):
            try:
                client = OpenAI()
                
                # Build the chat context for the AI model
                api_messages = [{"role": "system", "content": system_instruction}]
                for m in st.session_state.messages:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages
                )
                
                ai_response = response.choices.message.content
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Error communicating with AI. Check your OpenAI API key. Details: {e}")



      

           
        
   
                
            
                   
              
