# venturearchitect/agents/config.py

from google.adk.models.google_llm import Gemini
from google.genai import types

# Default Gemini model for all agents in this project
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"

# Shared retry configuration for robustness (rate limits, transient errors, etc.)
retry_config = types.HttpRetryOptions(
    attempts=5,          # max retries
    exp_base=7,          # exponential backoff base
    initial_delay=1,     # seconds
    http_status_codes=[429, 500, 503, 504],
)

def default_gemini_model() -> Gemini:
    """
    Factory function that returns a Gemini model instance
    with our standard retry configuration.
    """
    return Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    )
