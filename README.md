# 📡 OpticalGPT: Network XML Fault Analyzer

A user-friendly Streamlit web app for analyzing optical network alarm and performance monitoring (PM) XML files using either **local large language models (LLMs)** via **Ollama** or **OpenAI GPT-4o/gpt-4o-mini** via API.

---

## ✨ Features

- 🔼 Upload `alarm.xml`, `pm.xml`, and optional `topology.xml`
- 🤖 Choose between **local** (llama3/mistral) or **cloud-based** (GPT-4o/GPT-4o-mini) models
- 📄 Automatically:
  - Simplifies PM data (RX/TX metrics only)
  - Parses full alarm XML
  - Generates a network fault summary
  - Supports follow-up diagnosis via chatbot
- 💵 Cost tracking enabled for GPT usage
- 📥 Download results as `.txt` or `.md`

---

## 📂 Project Structure

```
.
├── alarm/                # Folder to store uploaded or default alarm XML
├── app.py                # Local Ollama-based app
├── app_expensive.py      # GPT-4o/4o-mini app with cost tracking
├── gpt_xml_analyzer.py   # GPTXMLAnalyzer class for OpenAI version
├── ollama_xml_analyzer.py# XML simplifier and summarizer for Ollama models
├── pm/                   # Folder for PM XML and summaries
├── topology/             # Optional topology XML folder
├── get/                  # Optional storage or log folder
└── README.md             # This file
```

---

## 🚀 Getting Started

You can choose between two ways to run OpticalGPT:

---

### 🔹 Method 1: Use Local LLM via Ollama (`app.py`)

> ✅ **Free** to use, no API key required  
> 💻 Runs entirely **locally** with `llama3` or `mistral`

#### 1. Install Ollama

Download and install from: [https://ollama.com](https://ollama.com)

#### 2. Pull a local model (once only)

```bash
ollama pull llama3
# or for smaller models:
ollama pull mistral
```

#### 3. Install Python dependencies

```bash
pip install streamlit requests
```

#### 4. Run the Streamlit App

```bash
streamlit run app.py
```

You will be able to:
- Upload XML files or use defaults (`alarm/`, `pm/`, `topology/`)
- Choose `llama3` or `mistral`
- View simplified PM + full alarm analysis
- Download results
- Chat with a local model

---

### 🔹 Method 2: Use OpenAI GPT Models (`app_expensive.py`)

> 🔐 Requires **OpenAI API Key**  
> 💡 Supports `gpt-4o` and `gpt-4o-mini` with **inference cost tracking**

#### 1. Get your OpenAI API Key

Create one at: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

#### 2. Install dependencies

```bash
pip install streamlit openai
```

#### 3. Run the GPT-Powered App

```bash
streamlit run app_expensive.py
```

#### 4. Features

- Upload XML or use defaults
- Automatically summarize alarm, PM, and topology data
- Estimate cost per GPT call (token usage based)
- Ask follow-up questions using chat with a GPT-powered agent

---

## 🧠 Model Options

| Model        | Description                               | Cost (approx.)          |
|--------------|-------------------------------------------|--------------------------|
| `llama3`     | Meta’s strong general LLM (local, free)   | ✅ Free (Ollama)         |
| `mistral`    | Small, fast local model                   | ✅ Free (Ollama)         |
| `gpt-4o`     | OpenAI's latest multimodal flagship model | 💵 Paid (OpenAI API)     |
| `gpt-4o-mini`| Lighter/faster GPT model from OpenAI      | 💵 Paid (cheaper tokens) |

---

## 📥 Downloads

- **PM Summary** and **Root-Cause Report** downloadable as `.txt` or `.md`
- Chat results display cost-per-response (if GPT is used)

---

## 🔒 Privacy

All analysis is done locally when using Ollama. No files are sent externally. If using OpenAI, data is sent securely via HTTPS.

---

## 📜 License

**MIT License** – free to use, share, and improve.
