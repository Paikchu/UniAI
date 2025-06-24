"""Configuration settings for the application"""
import json
import os
from dotenv import load_dotenv

load_dotenv()
from typing import Optional, List, Dict


class Settings:
    def __init__(self):
        self.prompts = self._load_prompts()
        self.models = self._load_models()

    def _load_prompts(self) -> Dict[str, str]:
        """Load system prompt configuration"""
        prompts_json = os.getenv("SYSTEM_PROMPTS", "{}")
        try:
            return json.loads(prompts_json)
        except json.JSONDecodeError:
            return {}

    def _load_models(self) -> List[str]:
        """Load supported model list"""
        models_json = os.getenv("SUPPORTED_MODELS", "[]")
        try:
            return json.loads(models_json)
        except json.JSONDecodeError:
            return ["deepseek-chat"]

    def get_prompt(self, scene_id: str) -> Optional[str]:
        """Get prompt by scene ID"""
        return self.prompts.get(scene_id)

    def is_model_supported(self, model: str) -> bool:
        """Check if model is supported"""
        return model in self.models


settings = Settings()
