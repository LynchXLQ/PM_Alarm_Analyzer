# -*- coding: utf-8 -*-
# @Time     : 4/8/2025 11:28 AM
# @Author   : Linqi Xiao
# @Software : PyCharm
# @Version  : python 3.12
# @Description : Class for simplifying XML and analyzing via local LLM (Ollama)

import requests
import os


class XMLSimplifier:
    def __init__(self, model="llama3", ollama_url="http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url

    def read_xml_as_text(self, file_name, folder="get"):
        file_path = os.path.join(folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def build_prompt(self, file_type, xml_text):
        instructions = {
            "alarm": """
You are a network fault XML simplifier.

Your task is to extract only meaningful and active alarms from the provided alarm XML. For each valid alarm, output the following fields **explicitly and completely**:

- Device name
- Port or interface name 
- Alarm type
- Severity
- Time (if available)
- Probable cause

IMPORTANT RULES:
- Only include alarms that contain **all six fields** above.
- Discard entries with status "cleared", "normal", or missing values.
- Do not include partial, placeholder, or unknown alarms.
- If any of the required fields are missing, skip that alarm.

Format the output in clean, plain English, grouped by device if applicable.

Here is the XML input:
""",
            "pm": """
You are a performance monitoring XML parser.

Your task is to extract and compress raw PM (performance monitoring) entries from the XML.

Extraction rules:
- Only extract PM entries where the "pm-type" contains **"input"** or **"output"**
- Ignore any entries where "pm-type" includes "avg", "min", or "max"
- For each entry, extract the following fields:
  - Interface name (if available)
  - Port name (if available)
  - PM type
  - PM value
  - Timestamp

Additional requirements:
- Do not perform any interpretation or filtering based on value thresholds
- Do not analyze or comment on the data
- Ensure every matching PM entry is extracted — do not skip any

Output format:
List each PM entry as a block of plain English with clearly labeled fields.
Group by device or circuit-pack if available.

Here is the XML input:
"""
        }
        return instructions[file_type] + "\n\nHere is the XML:\n\n" + xml_text

    def simplify(self, prompt):
        response = requests.post(f"{self.ollama_url}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]

    def save_summary(self, output_text, folder, file_name="summary.txt"):
        os.makedirs(folder, exist_ok=True)
        save_path = os.path.join(folder, file_name)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\nSimplified result saved to: {save_path}")

    def run(self, file_type, file_name, input_folder):
        xml_raw = self.read_xml_as_text(file_name, folder=input_folder)
        prompt = self.build_prompt(file_type, xml_raw)
        summary = self.simplify(prompt)

        print(f"=== Simplified Output for {file_type.upper()} ===")
        print(summary)

        self.save_summary(summary, folder=input_folder)

    def analyze_summary(self, alarm_xml_path="alarm/Ciena_ROADMA.xml", pm_summary_path="pm/summary.txt",
                        save_to="analysis.txt"):
        def load_file(path):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""

        # Load raw alarm XML (uncompressed)
        alarm_raw_xml = load_file(alarm_xml_path)

        # Load simplified PM summary
        pm_summary = load_file(pm_summary_path)

        prompt = f"""
You are a fault diagnosis expert in optical transport networks.

The following is a full alarm XML and a simplified summary of PM data. Your job is to analyze and diagnose what might be going wrong in the network.

=== ALARM XML (full) ===
{alarm_raw_xml}

=== PM SUMMARY ===
{pm_summary}

Please answer the following:
1. What devices or ports show critical issues?
2. What are the most likely root causes of the problems?
3. What troubleshooting actions would you recommend?

Organize your answer in sections:
- Observations
- Probable Causes
- Suggested Actions
"""

        result = self.simplify(prompt)

        print("\n=== Diagnostic Analysis ===")
        print(result)

        with open(save_to, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\nAnalysis result saved to: {save_to}")


if __name__ == "__main__":
    simplifier = XMLSimplifier(model="llama3")

    # Step 1: 提取性能监控（PM）内容，保存 summary
    simplifier.run(file_type='pm', file_name="Ciena_ROADMA.xml", input_folder="pm")

    # Step 2: 不提取 alarm，直接传入原始 alarm XML + PM summary，分析问题
    simplifier.analyze_summary(
        alarm_xml_path="alarm/Ciena_ROADMA.xml",
        pm_summary_path="pm/summary.txt",
        save_to="analysis.txt"
    )
