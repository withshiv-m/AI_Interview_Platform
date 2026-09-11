import json
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class LLMServiceError(Exception):
    pass


class LLMService:
    """Small provider-neutral wrapper for OpenAI-compatible chat APIs."""

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "").strip()
        self.model = os.getenv("LLM_MODEL", "").strip()
        self.api_url = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions").strip()
        self.timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

    @property
    def enabled(self):
        return bool(self.api_key and self.model)

    def request_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        if not self.enabled:
            raise LLMServiceError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL, or use demo fallback mode.")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            data = json.loads(content)
            if not isinstance(data, dict):
                raise ValueError("LLM response is not a JSON object")
            return data
        except requests.RequestException as exc:
            raise LLMServiceError(f"LLM request failed: {exc}") from exc
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            raise LLMServiceError(f"Invalid structured LLM response: {exc}") from exc
