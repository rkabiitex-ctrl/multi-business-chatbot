import os
import csv
import io
from datetime import datetime

import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Universal AI Business Suite",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# PROFESSIONAL DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: #0b0e13;
    color: #f4f5f7;
}

[data-testid="stSidebar"] {
    background: #141923;
    border-right: 1px solid #303744;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #4c4328;
    background: linear-gradient(120deg, #20232b, #171912);
    margin-bottom: 25px;
}

.hero h1 {
    color: #f2d780;
    font-size: clamp(28px, 4vw, 46px);
    font-weight: 800;
}

.hero p {
    color: #c6ccd5;
    font-size: 16px;
}

.section {
    background: #171c25;
    padding: 22px;
    border: 1px solid #303744;
    border-radius: 16px;
    margin-bottom: 18px;
}

div[data-testid="stMetric"] {
    background: #171c25;
    border: 1px solid #303744;
    border-radius: 14px;
    padding: 16px;
}

div[data-testid="stMetricValue"] {
    color: #f2d780;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 700;
}

div.stButton > button[kind="primary"] {
    background: #d8b65a;
    color: #111319;
    border: none;
}

div.stButton > button[kind="primary"]:hover {
    background: #f2d780;
    color: #111319;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

hr {
    border-color: #303744;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# BUSINESS PROFILES
# --------------------------------------------------

PROFILES = {
    "Dental Clinic": (
        "Dental Receptionist",
        "Welcome to our dental clinic! Would you like to book a cleaning, "
        "consultation, or another dental service?"
    ),
    "Salon & Barber": (
        "Salon Booking Assistant",
        "Welcome! Which service would you like to book: a haircut, styling, "
        "braiding, or another service?"
    ),
    "Hotel & Guest House": (
        "Hospitality Assistant",
        "Welcome! I can help with a room enquiry. What dates are you "
        "considering, and how many guests will be staying?"
    ),
    "Real Estate": (
        "Property Enquiry Assistant",
        "Welcome! Are you looking to rent, buy, or sell a property?"
    ),
    "Retail Store": (
        "Retail Sales Assistant",
        "Welcome to our store! Which product are you interested in?"
    ),
    "General Business": (
        "Customer Service Assistant",
        "Hello! Thank you for contacting us. What service can we help you with?"
    ),
}


# --------------------------------------------------
# SESSION DATA
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "leads" not in st.session_state:
    st.session_state.leads = []

if "case_result" not in st.session_state:
    st.session_state.case_result = ""


def get_ai_client():
    """Read the API key from Streamlit secrets or environment."""
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        key = ""

    key = key or os.getenv("OPENAI_API_KEY", "")

    if key and OpenAI:
        return OpenAI(api_key=key)

    return None


def ask_ai(system_prompt, user_prompt):
    """Return an AI response, or None when AI is not configured."""
    client = get_ai_client()

    if client is None:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown("# ✨ Universal AI")
    st.caption("BUSINESS AUTOMATION SUITE")
    st.divider()

    page = st.radio(
        "WORKSPACE NAVIGATION",
        [
            "AI Lead Booking Agent",
            "Legal & Judicial Case Analyzer",
            "Lead Dashboard",
            "Settings & Help",
        ],
    )

    st.divider()
    st.markdown("### 💼 Business Packages")
    st.markdown("**Standard Package**")
    st.write("For clinics, shops, salons and service businesses.")
    st.caption(
        "Choose pricing based on your costs and the services "
        "you actually provide."
    )

    st.divider()
    st.caption("Prototype version · Built with Streamlit")


# --------------------------------------------------
# PAGE 1: BOOKING AGENT
# --------------------------------------------------

if page == "AI Lead Booking Agent":

    st.markdown("""
    <div class="hero">
        <h1>✨ Universal AI Business Booking Agent</h1>
        <p>
            A smarter way to handle enquiries, organise customer requests,
            and help businesses capture new leads.
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_leads = len(st.session_state.leads)

    c1, c2, c3 = st.columns(3)

    c1.metric("Business Profiles", len(PROFILES))
    c2.metric("Saved Lead Requests", total_leads)
    c3.metric(
        "AI Status",
        "Connected" if get_ai_client() else "Demo Mode"
    )

    st.markdown("### Choose Your Business")

    profile = st.selectbox(
        "AI Agent Profile",
        list(PROFILES.keys()),
    )

    role, greeting = PROFILES[profile]

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(f"#### 🤖 {role}")
    st.info(greeting)

    st.markdown("### Customer Conversation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input(
        "Type a customer message here..."
    )

    if user_message:
        st.session_state.messages.append({
            "role": "user",
            "content": user_message,
        })

        history = "\n".join(
            f'{m["role"]}: {m["content"]}'
            for m in st.session_state.messages[-10:]
        )

        answer = ask_ai(
            f"""
            You are a friendly and professional {role}.
            Help customers explain what service they need.
            Ask one useful follow-up question at a time.
            Collect relevant booking preferences and contact details.
            Never claim a booking is confirmed or a calendar was checked.
            Never request passwords or payment card details.
            Keep your response under 100 words.
            """,
            history,
        )

        if answer is None:
            answer = (
                "Thank you for your message! I can help prepare your "
                "booking request. Please tell me which service you need "
                "and your preferred date or time."
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
        })

        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Lead Request", type="primary",
                     use_container_width=True):

            if not st.session_state.messages:
                st.warning("Start a conversation before saving a lead.")
            else:
                transcript = "\n".join(
                    f'{m["role"]}: {m["content"]}'
                    for m in st.session_state.messages
                )

                st.session_state.leads.append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Business": profile,
                    "Status": "New",
                    "Conversation": transcript,
                })

                st.success("Lead request saved for this session.")

    with col2:
        if st.button("🗑️ Clear Conversation",
                     use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Lead Capture Checklist")

    st.write("- Service or product requested")
    st.write("- Preferred appointment date and time")
    st.write("- Customer name, if needed")
    st.write("- Contact details, with appropriate consent")
    st.write("- Confirmation by the actual business")


# --------------------------------------------------
# PAGE 2: LEGAL ANALYZER
# --------------------------------------------------

elif page == "Legal & Judicial Case Analyzer":

    st.markdown("""
    <div class="hero">
        <h1>⚖️ Legal & Judicial Case Analyzer</h1>
        <p>
            Organise legal documents, summarise testimony, and identify
            questions that require further review.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "This tool provides document organisation and general information, "
        "not legal advice. Do not enter confidential information without "
        "appropriate permission and data protections."
    )

    jurisdiction = st.text_input(
        "Country or jurisdiction (optional)",
        placeholder="For example: Uganda",
    )

    case_text = st.text_area(
        "Paste Case Legal Text Here",
        height=260,
        placeholder="Paste case details, testimony, or a legal document...",
    )

    if st.button("⚖️ Run Legal Analysis", type="primary",
                 use_container_width=True):

        if len(case_text.strip()) < 40:
            st.error("Please enter more case text to analyse.")
        else:
            with st.spinner("Organising the case information..."):

                result = ask_ai(
                    """
                    You help organise legal documents for general information.
                    Do not provide definitive legal advice.
                    Do not invent laws, citations, or court decisions.
                    Separate allegations from facts established in the text.
                    State when the jurisdiction or information is missing.
                    Return these sections:
                    1. Plain-language summary
                    2. Parties and important events
                    3. Evidence mentioned
                    4. Questions and missing information
                    5. Questions for a qualified lawyer
                    6. Limitations and disclaimer
                    """,
                    f"Jurisdiction: {jurisdiction or 'Not specified'}\n\n"
                    f"Document:\n{case_text}",
                )

                if result is None:
                    result = f"""
### Preliminary Case Summary

{case_text[:1800]}

### Details to Verify

- Identify the parties and relevant dates.
- Distinguish allegations from established facts.
- Check which evidence and witnesses are mentioned.
- Identify missing information and unanswered questions.
- Confirm the applicable jurisdiction and relevant law.

### Questions for Further Review

- What legal issue needs to be examined?
- Are supporting documents available?
- What additional facts could change the analysis?

### Important Disclaimer

This is a basic document-organising demonstration, not legal
advice or a prediction of a court outcome. Consult a qualified
lawyer about the full facts and applicable law.
"""

                st.session_state.case_result = result

    if st.session_state.case_result:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown(st.session_state.case_result)

        st.download_button(
            "📥 Download Analysis",
            data=st.session_state.case_result,
            file_name="case_analysis.md",
            mime="text/markdown",
        )

        st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE 3: LEAD DASHBOARD
# --------------------------------------------------

elif page == "Lead Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>📊 Lead Management Dashboard</h1>
        <p>Review and export customer requests collected by your agent.</p>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Total Lead Requests", len(st.session_state.leads))

    if st.session_state.leads:

        st.dataframe(
            st.session_state.leads,
            use_container_width=True,
            hide_index=True,
        )

        output = io.StringIO()

        writer = csv.DictWriter(
            output,
            fieldnames=st.session_state.leads[0].keys(),
        )

        writer.writeheader()
        writer.writerows(st.session_state.leads)

        st.download_button(
            "📥 Export Leads to CSV",
            data=output.getvalue(),
            file_name="business_leads.csv",
            mime="text/csv",
            type="primary",
        )

        if st.button("Clear Session Leads"):
            st.session_state.leads = []
            st.rerun()

    else:
        st.info(
            "No leads saved yet. Start a conversation in the Booking "
            "Agent and click Save Lead Request."
        )

    st.caption(
        "Current limitation: session leads are temporary. A database "
        "is required for permanent business records."
    )


# --------------------------------------------------
# PAGE 4: SETTINGS AND HELP
# --------------------------------------------------

elif page == "Settings & Help":

    st.markdown("""
    <div class="hero">
        <h1>⚙️ Settings & Help</h1>
        <p>Configure your app and prepare it for real businesses.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### AI Configuration")

    if get_ai_client():
        st.success("An AI API key is configured.")
    else:
        st.info(
            "The app is running in demo mode. To enable AI responses, "
            "configure an API key in Streamlit secrets."
        )

    st.markdown("### Deployment")

    st.code(
        "pip install -r requirements.txt\n"
        "streamlit run app.py",
        language="bash",
    )

    st.markdown("### Recommended Next Upgrades")

    st.markdown("""
    - Permanent database for lead records.
    - Secure login and separate business accounts.
    - Real calendar and appointment integrations.
    - Email or SMS notifications.
    - Privacy policy and customer-data protection.
    - Automated testing and error monitoring.
    - Clear legal disclaimers and professional review.
    """)

    st.markdown("### Important")

    st.write(
        "Never put API keys directly into app.py or commit them to "
        "GitHub. Store secrets in Streamlit Community Cloud settings."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Universal AI Business Suite | Prototype | "
    "Verify results before using them for business or legal decisions."
)
