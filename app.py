import streamlit as st
from openai import OpenAI

# ---- CONFIG ----
st.set_page_config(page_title="Sentry Signal AI", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0f0b1f;
        color: #f5f3ff;
    }

    section[data-testid="stSidebar"] {
        background-color: #17112b;
        border-right: 1px solid #2a2147;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    h1, h2, h3 {
        color: #f5f3ff;
        letter-spacing: -0.02em;
    }

    p, label, div {
        color: #d6d0eb;
    }

    .stTextArea textarea {
        background-color: #17112b !important;
        color: #f5f3ff !important;
        border: 1px solid #3a2f63 !important;
        border-radius: 10px !important;
        font-family: monospace;
    }

    .stTextInput input {
        background-color: #17112b !important;
        color: #f5f3ff !important;
        border: 1px solid #3a2f63 !important;
        border-radius: 10px !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6d59ff, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        filter: brightness(1.08);
    }

    [data-testid="stMetric"] {
        background-color: #17112b;
        border: 1px solid #2a2147;
        padding: 1rem;
        border-radius: 14px;
    }

    .sentry-card {
        background-color: #17112b;
        border: 1px solid #2a2147;
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 0 1px rgba(255,255,255,0.02);
    }

    .sentry-kicker {
        color: #8b7bd6;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    .sentry-hero {
        background: linear-gradient(180deg, #17112b 0%, #120d24 100%);
        border: 1px solid #2a2147;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
<div class="sentry-hero">
    <div class="sentry-kicker">AI Observability Prototype</div>
    <h1>🧠 Sentry Signal AI</h1>
    <p>Turn grouped production errors into developer pain points, messaging, and campaign ideas.</p>
</div>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

persona = st.sidebar.selectbox(
    "Target Persona",
    ["Frontend Developer", "Backend Developer", "Full-Stack Developer"]
)

tone = st.sidebar.selectbox(
    "Output Style",
    ["Technical", "Marketing", "Executive"]
)

# ---- SAMPLE DATA ----
sample_logs = """
[Frontend - React]
TypeError: Cannot read property 'map' of undefined
React hydration failed: UI mismatch during server render
Unhandled promise rejection in componentDidMount

[Backend - API]
500 Internal Server Error on /api/users
Database connection timeout after 10 seconds
Failed to serialize response payload

[GraphQL]
Cannot return null for non-nullable field Query.user
Resolver failed for getUserProfile

[Performance]
Memory leak detected in component lifecycle
Slow query execution (>5s)
High CPU usage during request processing
"""

if st.button("✨ Use Sample Sentry Data"):
    st.session_state["logs"] = sample_logs

# ---- INPUT ----
user_input = st.text_area(
    "📋 Paste Error Logs or Issues",
    value=st.session_state.get("logs", ""),
    height=200
)

# ---- METRICS (for demo effect) ----
col1, col2, col3 = st.columns(3)
col1.metric("Errors Analyzed", "1,248")
col2.metric("Patterns Detected", "6")
col3.metric("Insights Generated", "12")

# ---- MAIN ACTION ----
if st.button("🚀 Generate Insights"):

    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_input.strip():
        st.error("Please enter some error logs.")
    else:
        client = OpenAI(api_key=api_key)

        with st.spinner("Analyzing errors and generating insights..."):

            prompt = f"""
            You are a senior product marketing manager at a developer tools company like Sentry.

            Analyze the following error logs and generate structured insights.

            Target persona: {persona}
            Tone: {tone}

            Do the following:

            1. Summarize the key issues
            2. Cluster into 3–5 themes
            3. Translate into developer pain points
            4. Suggest:
               - 3 blog post ideas
               - 2 marketing campaign ideas
               - Messaging angles

            Keep it concise, structured, and insightful.

            Error logs:
            {user_input}
            """

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content

        # ---- OUTPUT ----
        st.success("Insights generated")
        
        st.markdown('<div class="sentry-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Generated Insights")
        st.markdown(response.choices[0].message.content)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
    label="📄 Export Insights",
    data=response.choices[0].message.content,
    file_name="sentry_insights.txt",
    mime="text/plain"
)



# ---- FOOTER ----
st.markdown("---")
st.caption("Built as a prototype to explore how observability data can power marketing insights.")
