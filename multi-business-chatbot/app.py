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
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<h2 class="gold-text">🧭 Workspace Navigation</h2>', unsafe_allow_html=True)
app_mode = st.sidebar.radio("Go to Page:", ["🤖 AI Lead Booking Agent", "⚖️ Judicial Case Analyzer"])
st.sidebar.divider()

if app_mode == "🤖 AI Lead Booking Agent":
    st.markdown('<h1 class="gold-text">🤖 Universal AI Business Booking Agent</h1>', unsafe_allow_html=True)
    business_type = st.selectbox("Choose an AI Agent Profile to Demo:", ["Global Dental Clinic Receptionist", "Elite Med-Spa & Cosmetics Concierge", "General ChatGPT AI Workspace"])

    if business_type == "Global Dental Clinic Receptionist":
        system_instruction, welcome_message = "You are a dental clinic receptionist. Get their phone to book.", "Hello! Ready to book a cleaning?"
    elif business_type == "Elite Med-Spa & Cosmetics Concierge":
        system_instruction, welcome_message = "You are an elite med-spa concierge. Ask for phone or WhatsApp.", "Welcome to our premier aesthetics concierge. ✨"
    else:
        system_instruction, welcome_message = "You are ChatGPT, a highly helpful assistant. Provide value.", "Welcome to your General ChatGPT AI Workspace! 🚀"

    if "messages" not in st.session_state or st.sidebar.button("Reset Chat"):
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "audio" in msg: st.audio(msg["audio"], format="audio/mp3")

    user_message = st.chat_input("Type your message here manually...")
    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        try:
            client = OpenAI()
            api_messages = [{"role": "system", "content": system_instruction}]
            for m in st.session_state.messages:
                if m["role"] in ["user", "assistant"]:
                    api_messages.append({"role": m["role"], "content": str(m["content"])})
            response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages)
            ai_text = response.choices[0].message.content
            audio_resp = client.audio.speech.create(model="tts-1", voice="alloy", input=ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": audio_resp.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

elif app_mode == "⚖️ Judicial Case Analyzer":
    st.markdown('<h1 class="gold-text">⚖️ Legal & Judicial Case Analyzer</h1>', unsafe_allow_html=True)
    case_text = st.text_area("Paste Case Legal Text Here:", height=250)
    if st.button("🔥 Run AI Judicial Analysis") and case_text:
        try:
            client = OpenAI()
            instruction = "You are a senior judicial counsel. Analyze the text into: Facts, Claims, Laws, and Recommendations."
            resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": instruction}, {"role": "user", "content": case_text}])
            st.info(resp.choices[0].message.content)
        except Exception as e:
            st.error(f"Analysis Error: {e}")
