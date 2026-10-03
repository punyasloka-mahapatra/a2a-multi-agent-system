import os

from dotenv import load_dotenv

load_dotenv()


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

CLASSIFIER_MODEL = os.getenv(
    "CLASSIFIER_MODEL",
    "llama3.2"
)

RESOLUTION_MODEL = os.getenv(
    "RESOLUTION_MODEL",
    "llama3.2"
)

RESPONSE_MODEL = os.getenv(
    "RESPONSE_MODEL",
    "llama3.2"
)

CLASSIFIER_URL = os.getenv(
    "CLASSIFIER_URL",
    "http://localhost:8001"
)

RESOLUTION_URL = os.getenv(
    "RESOLUTION_URL",
    "http://localhost:8002"
)

RESPONSE_URL = os.getenv(
    "RESPONSE_URL",
    "http://localhost:8003"
)