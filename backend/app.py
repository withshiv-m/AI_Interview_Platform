import streamlit as st

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening & Job Matching")
st.write("Multi-Agent Resume Screening Platform")

st.divider()

st.header("Welcome 👋")

st.write(
    "Upload resumes and job descriptions "
    "to find the best candidate matches."
)