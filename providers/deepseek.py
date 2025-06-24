import os
from typing import Optional

import requests

from core.exceptions import ProviderException


class DeepSeekResponse:
    """Mock response object to match langchain interface"""

    def __init__(self, content: str, response_metadata: dict = None):
        self.content = content
        self.response_metadata = response_metadata or {}


def get_deepseek_response(
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 100
) -> DeepSeekResponse:
    """Call DeepSeek API to get response"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ProviderException("DeepSeek API key not found")

    # Prepare messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Prepare request payload
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Make API request to DeepSeek
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Extract usage information
        usage = data.get("usage", {})
        response_metadata = {
            "token_usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            },
            "model_name": data.get("model", "deepseek-chat")
        }

        return DeepSeekResponse(content=content, response_metadata=response_metadata)

    except requests.exceptions.RequestException as e:
        raise ProviderException(f"DeepSeek API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ProviderException(f"Invalid DeepSeek API response format: {str(e)}")
    except Exception as e:
        raise ProviderException(f"Unexpected error calling DeepSeek API: {str(e)}")
