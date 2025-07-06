import streamlit as st
import os


st.set_page_config(page_title="DevOps AI Agent Dashboard", layout="wide")


st.title("DevOps + AI Monitoring Agent")


cpu_file = "cpu_status.txt"
cpu_usage = "Unknown"
if os.path.exists(cpu_file):
    with open(cpu_file, "r") as f:
        cpu_usage = f.read().strip()
st.metric("Current CPU Usage", f"{cpu_usage}%")


llm_file = "last_analysis.txt"
if os.path.exists(llm_file):
    with open(llm_file, "r") as f:
        llm_output = f.read().strip()
    st.subheader("Last Root Cause (LLM Output)")
    st.code(llm_output)
else:
    st.warning("No LLM analysis recorded yet.")


log_file = "remediation_log.txt"
st.subheader("Remediation Log")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        st.text(f.read())
else:
    st.info("No remediation actions logged yet.")
