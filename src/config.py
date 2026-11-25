from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
from exceptions import ConfigError

ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    api_url: str
    api_key: str
    model_name: str
    timeout: int = 60
    temperature: float = 0.2
    max_tokens: int = 512
    system_prompt: str = "Você é um assistente objetivo e claro. Responda em português."


def load_config() -> AppConfig:
    load_dotenv(dotenv_path=ROOT_DIR / ".env")

    api_url = os.getenv("LLM_API_URL", "").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model_name = os.getenv("LLM_MODEL_NAME", "").strip()
    timeout_raw = os.getenv("LLM_TIMEOUT", "60").strip()
    temperature_raw = os.getenv("LLM_TEMPERATURE", "0.2").strip()
    max_tokens_raw = os.getenv("LLM_MAX_TOKENS", "512").strip()
    system_prompt = os.getenv(
        "LLM_SYSTEM_PROMPT",
        "Você é um assistente objetivo e claro. Responda em português.",
    ).strip()

    if not api_url:
        raise ConfigError("Configuração ausente: defina 'LLM_API_URL' no arquivo .env.")
    if not api_key:
        raise ConfigError("Configuração ausente: defina 'LLM_API_KEY' no arquivo .env.")
    if not model_name:
        raise ConfigError("Configuração ausente: defina 'LLM_MODEL_NAME' no arquivo .env.")

    try:
        timeout = int(timeout_raw)
        if timeout <= 0:
            raise ValueError
    except ValueError as exc:
        raise ConfigError("Configuração inválida: 'LLM_TIMEOUT' deve ser um inteiro positivo.") from exc

    try:
        temperature = float(temperature_raw)
        if not (0.0 <= temperature <= 2.0):
            raise ValueError
    except ValueError as exc:
        raise ConfigError("Configuração inválida: 'LLM_TEMPERATURE' deve estar entre 0.0 e 2.0.") from exc

    try:
        max_tokens = int(max_tokens_raw)
        if max_tokens <= 0:
            raise ValueError
    except ValueError as exc:
        raise ConfigError("Configuração inválida: 'LLM_MAX_TOKENS' deve ser um inteiro positivo.") from exc

    return AppConfig(
        api_url=api_url,
        api_key=api_key,
        model_name=model_name,
        timeout=timeout,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
    )