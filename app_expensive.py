import streamlit as st
from gpt_xml_analyzer import GPTXMLAnalyzer
from pathlib import Path

st.set_page_config(page_title="GPT XML Network Analyzer", layout="wide")
st.title("📡 GPT XML Network Analyzer")

# --- API Key ---
api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

# --- Model Choice ---
col1, col2 = st.columns(2)
with col1:
    model_summary = st.selectbox("Model for Summary", ["gpt-4o", "gpt-4o-mini"], index=0)
with col2:
    model_chat = st.selectbox("Model for Chat", ["gpt-4o-mini", "gpt-4o"], index=0)

# --- Option Toggles ---
col1, col2 = st.columns(2)
with col1:
    use_defaults = st.checkbox("📂 Use default local files if not uploading", value=True)
with col2:
    show_cost = st.checkbox("💵 Show token usage cost", value=True)

# --- File Uploads ---
alarm_file = st.file_uploader("📁 Upload Alarm XML", type="xml", key="alarm")
pm_file = st.file_uploader("📁 Upload PM XML", type="xml", key="pm")
topo_file = st.file_uploader("📁 Upload Topology XML (optional)", type="xml", key="topo")

# --- Run Summary ---
if st.button("🚀 Run Summary and Analyze"):
    if not api_key or (not use_defaults and not (alarm_file or pm_file)):
        st.warning("Please provide API key and at least Alarm and PM XML files or enable default usage.")
    else:
        with st.spinner("Running GPT-4o summarization..."):
            for folder, file in zip(["alarm", "pm", "topology"], [alarm_file, pm_file, topo_file]):
                if file:
                    Path(folder).mkdir(exist_ok=True)
                    with open(Path(folder) / file.name, "wb") as f:
                        f.write(file.read())

            analyzer = GPTXMLAnalyzer(api_key, model_summary=model_summary, model_chat=model_chat)
            analyzer.summarize_all()

            st.session_state.analyzer = analyzer
            summary = analyzer.summary_text

            st.subheader("📄 Summary Result")
            st.text_area("Summary Text", summary, height=300)
            if show_cost:
                cost = analyzer.get_last_cost()
                st.success(f"✅ Summary completed. Cost: ${cost:.6f} USD")

# --- Chat Interface ---
st.divider()

if "analyzer" in st.session_state:
    st.subheader("💬 Chat with GPT")

    # Temporary variable to pre-fill input box
    if "preset_question" not in st.session_state:
        st.session_state.preset_question = ""

    st.markdown("💡 Sample questions:")
    col1, col2 = st.columns(2)
    for i, q in enumerate(st.session_state.analyzer.get_sample_questions()):
        if i % 2 == 0:
            if col1.button(q):
                st.session_state.preset_question = q
        else:
            if col2.button(q):
                st.session_state.preset_question = q

    # Input field with value from preset, but no session_state key to avoid conflict
    user_input = st.text_input("Ask your network question:", value=st.session_state.preset_question)
    st.session_state.preset_question = ""  # Clear after showing

    if user_input:
        with st.spinner("GPT is thinking..."):
            response = st.session_state.analyzer.chat(user_input)

            # Save to session chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Show chat bubbles
    if "chat_history" in st.session_state:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.get("show_cost", False):
            st.info(f"💵 This message cost: ${st.session_state.analyzer.get_last_cost():.6f} USD")
