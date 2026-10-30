import streamlit as st

# 1. Force sidebar navigation options
page_selection = st.sidebar.radio(
    "Go to Page:",
    ["AI Lead Booking Agent", "Judicial Case Analyzer", "BuildMost Sourcing Hub"],
    key="workspace_navigation"
)

# 2. Main content area rendering block
if page_selection == "AI Lead Booking Agent":
    st.title("AI Lead Booking Agent")
    try:
        # Import or call your specific agent function here
        # e.g., import booking_agent; booking_agent.run()
        st.write("Booking Agent content goes here.")
    except Exception as e:
        st.error(f"Failed to load Booking Agent: {e}")

elif page_selection == "Judicial Case Analyzer":
    st.title("Judicial Case Analyzer")
    try:
        st.write("Judicial Analyzer content goes here.")
    except Exception as e:
        st.error(f"Failed to load Case Analyzer: {e}")

elif page_selection == "BuildMost Sourcing Hub":
    st.title("BuildMost Sourcing Hub")
    try:
        st.write("Sourcing Hub content goes here.")
    except Exception as e:
        st.error(f"Failed to load Sourcing Hub: {e}")
