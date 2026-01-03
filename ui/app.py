import streamlit as st
import requests
import re

API_URL = "http://localhost:7071/api/analyze_repo"

st.set_page_config(
    page_title="Guardian Angel X-Crypto",
    page_icon="🛡",
    layout="centered"
)

# ---------------- Header ----------------
st.title("🛡 Guardian Angel X-Crypto")
st.caption("Preventing supply-chain attacks before code reaches production")

st.markdown("---")

# ---------------- Input ----------------
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repository"
)

analyze_btn = st.button("🔍 Analyze Latest Commit")

# ---------------- Validation ----------------
def is_valid_github_url(url):
    pattern = r"^https:\/\/github\.com\/[^\/]+\/[^\/]+$"
    return re.match(pattern, url)

# ---------------- Action ----------------
if analyze_btn:
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    if not is_valid_github_url(repo_url):
        st.error("Invalid GitHub repository URL format.")
        st.stop()

    with st.spinner("Analyzing repository for supply-chain risks..."):
        try:
            response = requests.get(
                API_URL,
                params={"repo": repo_url},
                timeout=30
            )
            data = response.json()
        except Exception as e:
            st.error(f"Failed to contact analysis engine: {e}")
            st.stop()

    st.markdown("---")

    # ---------------- Risk Summary ----------------
    risk = data["risk"]["risk"]
    confidence = data["risk"]["confidence"]

    color = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🔴"
    }[risk]

    st.subheader(f"{color} Risk Level: {risk}")
    st.caption(f"Confidence: {confidence}")

    col1, col2 = st.columns(2)
    col1.metric("Behavior Score", data["behavior_score"])
    col2.metric("Average Entropy", data["crypto_analysis"]["avg_entropy"])

    # ---------------- Explanation ----------------
    st.markdown("### 🧠 Why this result?")
    for reason in data.get("explanation", ["No anomalous activity detected"]):
        st.success(reason)

    # ---------------- Technical Details ----------------
    with st.expander("🔎 Show technical details"):
        st.json(data)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Guardian Angel X-Crypto • Industrial DevSecOps Security Tool")

