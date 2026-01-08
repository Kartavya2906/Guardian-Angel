import streamlit as st
import requests

API_URL = "http://localhost:7071/api/analyze_repo"

st.set_page_config(
    page_title="Guardian Angel X-Crypto",
    layout="centered"
)

st.title("🛡 Guardian Angel X-Crypto")
st.subheader("GitHub Supply Chain Security Scanner")

# ---------- Session State ----------
if "result" not in st.session_state:
    st.session_state.result = None

# ---------- Input ----------
repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/psf/requests"
)

# ---------- Button ----------
if st.button("🔍 Analyze GitHub Repo"):
    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL")
    else:
        with st.spinner("Analyzing repository..."):
            try:
                response = requests.get(
                    API_URL,
                    params={"repo": repo_url},
                    timeout=120
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.session_state.result = data

            except Exception as e:
                st.error(f"Engine unreachable: {e}")

# ---------- Display Result ----------
if st.session_state.result:
    st.success("Analysis complete")
    st.json(st.session_state.result)

