import requests
import json
from typing import Dict, Any


class LocalLLMClient:
    """Client for communicating with local Ollama instance running Qwen2.5-Coder."""

    def __init__(self, model_name: str = "qwen2.5-coder:7b-instruct-q4_K_M", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def analyze_code_snippet(self, code_snippet: str) -> Dict[str, Any]:
        prompt = f"""
You are an expert secure coding assistant and code reviewer. Analyze the following Python code snippet for security vulnerabilities (e.g. injection flaws, insecure deserialization, hardcoded secrets, poor error handling) and performance anti-patterns.

Return your response strictly in valid JSON format with the following keys:
- "vulnerable": boolean
- "severity": string ("LOW", "MEDIUM", "HIGH", "CRITICAL")
- "issues": list of strings describing the vulnerabilities
- "refactored_code": string containing the complete corrected code snippet

Code to analyze:
{code_snippet}
"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()

        result_text = response.json().get("response", "{}")
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {
                "vulnerable": False,
                "severity": "LOW",
                "issues": ["Failed to parse model JSON response."],
                "refactored_code": code_snippet
            }
