"""
Configuration Module
Handles loading configuration from environment variables with fallbacks.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default fallback."""
    return os.getenv(key, default)


def get_env_float(key: str, default: float) -> float:
    """Get environment variable as float with default fallback."""
    try:
        return float(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


def get_env_int(key: str, default: int) -> int:
    """Get environment variable as int with default fallback."""
    try:
        return int(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


class Config:
    """Application configuration with environment variable support."""
    
    # Model A Configuration
    MODEL_A_API_KEY = get_env("MODEL_A_API_KEY") or get_env("OPENAI_API_KEY")
    MODEL_A_BASE_URL = get_env("MODEL_A_BASE_URL") or None
    MODEL_A_NAME = get_env("MODEL_A_NAME", "gpt-4.1-mini")
    MODEL_A_NICKNAME = get_env("MODEL_A_NICKNAME", "Alice")
    MODEL_A_PERSONA = get_env(
        "MODEL_A_PERSONA",
        "You are a thoughtful and analytical assistant who enjoys exploring ideas in depth."
    )
    
    # Model B Configuration
    MODEL_B_API_KEY = get_env("MODEL_B_API_KEY") or get_env("OPENAI_API_KEY")
    MODEL_B_BASE_URL = get_env("MODEL_B_BASE_URL") or None
    MODEL_B_NAME = get_env("MODEL_B_NAME", "gpt-4.1-nano")
    MODEL_B_NICKNAME = get_env("MODEL_B_NICKNAME", "Bob")
    MODEL_B_PERSONA = get_env(
        "MODEL_B_PERSONA",
        "You are a creative and curious assistant who likes to ask questions and challenge assumptions."
    )
    
    # Conversation Settings
    DISCUSSION_TOPIC = get_env(
        "DISCUSSION_TOPIC",
        "The impact of artificial intelligence on society"
    )
    MAX_TURNS = get_env_int("MAX_TURNS", 10)
    TEMPERATURE = get_env_float("TEMPERATURE", 0.7)
    TURN_DELAY = get_env_float("TURN_DELAY", 1.0)
    SYSTEM_PROMPT_FILE = get_env("SYSTEM_PROMPT_FILE", "system_prompt.txt")
    
    @classmethod
    def get_model_a_config(cls):
        """Get Model A configuration as dictionary."""
        return {
            'api_key': cls.MODEL_A_API_KEY,
            'base_url': cls.MODEL_A_BASE_URL,
            'name': cls.MODEL_A_NAME,
            'nickname': cls.MODEL_A_NICKNAME,
            'persona': cls.MODEL_A_PERSONA
        }
    
    @classmethod
    def get_model_b_config(cls):
        """Get Model B configuration as dictionary."""
        return {
            'api_key': cls.MODEL_B_API_KEY,
            'base_url': cls.MODEL_B_BASE_URL,
            'name': cls.MODEL_B_NAME,
            'nickname': cls.MODEL_B_NICKNAME,
            'persona': cls.MODEL_B_PERSONA
        }
    
    @classmethod
    def get_conversation_config(cls):
        """Get conversation configuration as dictionary."""
        return {
            'discussion_topic': cls.DISCUSSION_TOPIC,
            'max_turns': cls.MAX_TURNS,
            'temperature': cls.TEMPERATURE,
            'turn_delay': cls.TURN_DELAY,
            'system_prompt_file': cls.SYSTEM_PROMPT_FILE
        }

