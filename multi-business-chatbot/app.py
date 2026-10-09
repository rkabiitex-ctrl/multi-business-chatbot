import streamlit as st
from openai import OpenAI

# 1. Setup the Web Page Layout
st.set_page_config(page_title="Universal AI Lead Booker", page_icon="🤖")
st.title("🤖 Universal AI Business Booking Agent")
st.write("Select a business category below to test how the AI adapts to capture customer leads.")

# 2. Dropdown Menu for Business Types
business_type = st.selectbox(
    "Choose a Business Type:",
    ["Apex Dentistry", "Elite Roofing & Solar", "Iron Pulse Gym", "Express Plumbing"]
)

# 3. Dynamically set the AI's Personality/Instructions based on selection
if business_type == "Apex Dentistry":
    system_instruction = "You are a friendly receptionist for Apex Dentistry. Answer basic dental questions politely. Your primary goal is to get the customer's phone number or email to book them a dental checkup."
    welcome_message = "Hello! Thanks for visiting Apex Dentistry. Are you looking to book a routine cleaning, or do you have a dental question?"

elif business_type == "Elite Roofing & Solar":
    system_instruction = "You are a professional sales assistant for Elite Roofing & Solar. Be confident and helpful. Your primary goal is to get the customer's address and phone number to schedule a free roof inspection."
    welcome_message = "Hi there! Welcome to Elite Roofing. Are you looking for a free estimate on a roof repair, solar installation, or a replacement?"

elif business_type == "Iron Pulse Gym":
    system_instruction = "You are an energetic, motivational assistant for Iron Pulse Gym. Be hyped up and encouraging. Your primary goal is to get the customer's email address to sign them up for a free 3-day workout pass."
    welcome_message = "Let's go! Welcome to Iron Pulse Gym. Ready to smash your fitness goals? Ask me anything about our membership plans or classes!"

elif business_type == "Express Plumbing":
    system_instruction = "You are an urgent, reliable customer agent for Express Plumbing. Be understanding and quick. Your primary goal is to get their phone number and a description of their issue so an emergency plumber can call them back immediately."
    welcome_message = "Express Plumbing here! Do you have an active leak, a clogged drain, or an emergency plumbing issue right now?"

st.divider()

# 4. Initialize Chat History in Streamlit Memory
if "messages" not in st.session_state or st.sidebar.button("Reset Chat"):
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

# Display the ongoing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Handle User Chat Input
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
