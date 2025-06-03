# app.py
# Streamlit GUI for XML-based network fault analysis

import streamlit as st
from ollama_xml_analyzer import XMLSimplifier
import os
import tempfile

st.set_page_config(page_title="Network XML Analyzer", layout="wide")
st.title("📡 Network XML Fault Analyzer")
st.markdown("Upload your **alarm**, **pm**, and optionally **topology** XML files to analyze network issues.")

# --- Model and LLM URL selector ---
model_choice = st.selectbox("Choose LLM Model", ["llama3", "mistral"], index=0)
ollama_url = st.text_input("Ollama API URL", value="http://localhost:11434")
simplifier = XMLSimplifier(model=model_choice, ollama_url=ollama_url)

# --- Upload section ---
alarm_file = st.file_uploader("Upload Alarm XML", type="xml", key="alarm")
pm_file = st.file_uploader("Upload PM XML", type="xml", key="pm")
topology_file = st.file_uploader("(Optional) Upload Topology XML", type="xml", key="topo")

run_button = st.button("🚀 Analyze Now")

if run_button:
    if not alarm_file or not pm_file:
        st.warning("Please upload at least Alarm and PM XML files.")
    else:
        with st.spinner("Analyzing XML data with LLM..."):
            # --- Temp directories ---
            os.makedirs("alarm", exist_ok=True)
            os.makedirs("pm", exist_ok=True)

            alarm_path = os.path.join("alarm", alarm_file.name)
            pm_path = os.path.join("pm", pm_file.name)

            with open(alarm_path, "wb") as f:
                f.write(alarm_file.read())

            with open(pm_path, "wb") as f:
                f.write(pm_file.read())

            # --- Run PM simplification ---
            simplifier.run(file_type='pm', file_name=pm_file.name, input_folder="pm")

            # --- Run full analysis ---
            simplifier.analyze_summary(
                alarm_xml_path=alarm_path,
                pm_summary_path="pm/summary.txt",
                save_to="analysis.txt"
            )

            # --- Display results ---
            with open("pm/summary.txt", "r", encoding="utf-8") as f:
                pm_summary = f.read()
            with open("analysis.txt", "r", encoding="utf-8") as f:
                analysis = f.read()
            with open(alarm_path, "r", encoding="utf-8") as f:
                alarm_raw = f.read()

            st.subheader("📄 PM Summary")
            st.text_area("Simplified PM Data", pm_summary, height=200)

            st.subheader("📄 Alarm XML")
            st.text_area("Full Alarm XML", alarm_raw, height=300)

            st.subheader("🧠 Analysis Result")
            st.markdown(analysis)

            # --- Download Buttons ---
            st.download_button("💾 Download Analysis (Text)", data=analysis, file_name="analysis.txt")
            st.download_button("📝 Download Analysis (Markdown)", data=f"### Diagnostic Analysis\n\n{analysis}",
                               file_name="analysis.md")
