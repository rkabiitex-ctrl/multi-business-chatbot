import streamlit as st
from playwright.sync_api import sync_playwright
from openai import OpenAI
import base64

st.set_page_config(page_title="GPT-4o Web Agent", page_icon="🤖", layout="centered")
st.title("🤖 GPT-4o Powered Web Agent")

# Securely pull your OpenAI key from Streamlit Secrets or a local file
# For local testing, you can replace this with OpenAI(api_key="your-key-here")
OPENAI_API_KEY = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

    url_input = st.text_input("Target URL:", "https://ycombinator.com")
    user_task = st.text_input("What should GPT-4o look for?", "Summarize the top 3 headlines")

    if st.button("Execute Task with GPT-4o", use_container_width=True):
        if not url_input.startswith("http"):
            url_input = f"https://{url_input}"
            
        with st.spinner("🌐 Launching Playwright browser backend..."):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_viewport_size({"width": 1280, "height": 800})
                
                try:
                    page.goto(url_input, timeout=30000)
                    st.success(f"Connected to: {page.title()}")
                    
                    # 1. Capture the page layout visually
                    screenshot_bytes = page.screenshot()
                    st.image(screenshot_bytes, caption="What the Agent Sees", use_container_width=True)
                    
                    # 2. Encode the image to Base64 format for OpenAI's Vision pipeline
                    base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
                    
                    # 3. Stream the vision payload directly to GPT-4o
                    with st.spinner("🧠 GPT-4o is executing vision analysis..."):
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": f"You are an AI browsing assistant. Analyze this webpage screenshot and fulfill the user's request: '{user_task}'"},
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:image/jpeg;base64,{base64_image}"
                                            }
                                        }
                                    ]
                                }
                            ]
                        )
                        
                        st.chat_message("assistant").write(response.choices[0].message.content)
                        
                except Exception as e:
                    st.error(f"Error handling request: {e}")
                finally:
                    browser.close()
else:
    st.info("🔑 Add your OpenAI API key in the sidebar to activate GPT-4o vision!")
