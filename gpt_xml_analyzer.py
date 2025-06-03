# -*- coding: utf-8 -*-
# @Author   : Linqi Xiao
# @Purpose  : GPTXMLAnalyzer with GPT-4o for summarization and GPT-4o-mini for interactive chat and cost tracking

from pathlib import Path
from openai import OpenAI


class GPTXMLAnalyzer:
    def __init__(self, api_key, model_summary="gpt-4o", model_chat="gpt-4o-mini"):
        self.api_key = api_key
        self.model_summary = model_summary
        self.model_chat = model_chat
        self.summary_text = ""
        self.chat_history = []
        self.last_cost = 0.0  # Store cost of last call

        self.client = OpenAI(api_key=api_key)

    def _read_single_file_from_folder(self, folder: str) -> str:
        folder_path = Path(folder)
        files = list(folder_path.glob("*.xml"))
        if not files:
            raise FileNotFoundError(f"No XML file found in {folder_path.resolve()}")
        return files[0].read_text(encoding="utf-8")

    def _chat_with_cost(self, model: str, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        output = response.choices[0].message.content

        usage = response.usage
        prompt_tokens = usage.prompt_tokens or 0
        completion_tokens = usage.completion_tokens or 0

        # Set pricing based on model
        if model.startswith("gpt-4o"):
            price_in = 0.005
            price_out = 0.01
        else:
            price_in = 0.002  # fallback defaults
            price_out = 0.004

        cost = (prompt_tokens / 1000) * price_in + (completion_tokens / 1000) * price_out
        self.last_cost = round(cost, 6)

        return output

    def summarize_all(self, alarm_folder="alarm", pm_folder="pm", topo_folder="topology", save_folder="summary"):
        alarm_xml = self._read_single_file_from_folder(alarm_folder)
        pm_xml = self._read_single_file_from_folder(pm_folder)
        topo_xml = self._read_single_file_from_folder(topo_folder)

        prompt = f"""
You are an expert in optical transport network diagnosis.

Below are the network data:

=== ALARM XML ===
{alarm_xml[:4000]}

=== PERFORMANCE MONITORING XML ===
{pm_xml[:4000]}

=== TOPOLOGY XML ===
{topo_xml[:6000]}

Task:
- Summarize critical PM issues (e.g., RX/TX anomalies, dropped signals)
- Extract key alarms (device, port, severity, cause)
- Cross-analyze with topology if possible
- Produce a brief network health summary
"""

        self.summary_text = self._chat_with_cost(self.model_summary, [
            {"role": "system", "content": "You are a helpful assistant for analyzing optical network health."},
            {"role": "user", "content": prompt}
        ])

        Path(save_folder).mkdir(parents=True, exist_ok=True)
        summary_path = Path(save_folder) / "summary.txt"
        summary_path.write_text(self.summary_text, encoding="utf-8")

        self.chat_history = [
            {"role": "system", "content": "You are a helpful assistant for diagnosing optical network faults."},
            {"role": "user",
             "content": f"Here is the latest summary of my network:\n{self.summary_text}\nYou will answer my follow-up questions based on this."}
        ]

    def chat(self, user_input: str) -> str:
        if not self.chat_history:
            raise RuntimeError("Please run summarize_all() first to initialize chat context.")

        self.chat_history.append({"role": "user", "content": user_input})
        answer = self._chat_with_cost(self.model_chat, self.chat_history)
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer

    def get_last_cost(self) -> float:
        return self.last_cost

    def get_sample_questions(self) -> list:
        return [
            "Which port on which ROADM is most likely causing the issue?",
            "What is the most probable root cause based on the alarms?",
            "Suggest step-by-step troubleshooting actions.",
            "Are there any critical RX/TX power anomalies?",
            "How do the alarms correlate with the topology?"
        ]
