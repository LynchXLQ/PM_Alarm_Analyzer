# 📡 Network XML Fault Analyzer

A user-friendly Streamlit web app for analyzing optical network alarm and performance monitoring (PM) XML files using local large language models (LLMs) via Ollama.

---

## ✨ Features

- 🔼 Upload `alarm.xml`, `pm.xml`, and optional `topology.xml`
- 🤖 Choose from local LLMs: `llama3` (default) or `mistral`
- 📄 Automatically:
  - Simplifies PM data (input/output metrics only)
  - Uses full alarm XML for analysis (not compressed)
  - Generates a root-cause analysis report
- 📥 Download results as `.txt` and `.md` files

---

## 🚀 Getting Started

### 1. Install Python dependencies

```bash
pip install streamlit requests
```

### 2. Install and start Ollama

Visit [https://ollama.com](https://ollama.com) and install the tool. Then pull at least one model:

```bash
ollama pull llama3
# or
ollama pull mistral
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 📂 Folder Structure

```
project/
├── app.py                  # Streamlit GUI
├── xml_simplifier.py       # Core XML-to-LLM logic
├── alarm/
│   └── alarm_file.xml
├── pm/
│   ├── pm_file.xml
│   └── summary.txt         # PM simplification output
├── analysis.txt            # Final fault analysis output
```

---

## 🧠 Model Info

| Model     | Description                      |
|-----------|----------------------------------|
| `llama3`  | Meta’s latest strong general LLM |
| `mistral` | Smaller, faster, and accurate    |

You can choose between them via dropdown in the interface.

---

## License

MIT – free to use, share and improve.
