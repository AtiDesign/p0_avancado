import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import load_config
from exceptions import ConfigError, InputValidationError
from llm_client import parse_response, prepare_request
from main import capture_input


class TestLocalLogic(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "LLM_API_URL": "http://localhost:11434/v1/chat/completions",
            "LLM_API_KEY": "chave-secreta-teste",
            "LLM_MODEL_NAME": "qwen3.5:4b",
            "LLM_TIMEOUT": "45",
            "LLM_TEMPERATURE": "0.7",
            "LLM_MAX_TOKENS": "256",
            "LLM_SYSTEM_PROMPT": "Responda em tópicos.",
        },
        clear=True,
    )
    def test_load_custom_generation_parameters(self):
        """Verifica se parâmetros de geração são carregados sem alterar o núcleo."""
        cfg = load_config()
        self.assertEqual(cfg.temperature, 0.7)
        self.assertEqual(cfg.max_tokens, 256)
        self.assertEqual(cfg.system_prompt, "Responda em tópicos.")

    @patch.dict(
        os.environ,
        {
            "LLM_API_URL": "http://localhost:11434/v1/chat/completions",
            "LLM_API_KEY": "chave-secreta-teste",
            "LLM_MODEL_NAME": "qwen3.5:4b",
            "LLM_TEMPERATURE": "3.5",
        },
        clear=True,
    )
    def test_invalid_temperature_raises_config_error(self):
        """Bloqueia temperatura fora da faixa permitida (0.0 a 2.0)."""
        with self.assertRaises(ConfigError):
            load_config()

    @patch.dict(
        os.environ,
        {
            "LLM_API_URL": "http://localhost:11434/v1/chat/completions",
            "LLM_API_KEY": "segredo-super-sensivel",
            "LLM_MODEL_NAME": "qwen3.5:4b",
            "LLM_TEMPERATURE": "0.3",
            "LLM_MAX_TOKENS": "128",
            "LLM_SYSTEM_PROMPT": "Sistema customizado",
        },
        clear=True,
    )
    def test_prepare_request_and_safe_logging(self):
        """Valida montagem do payload e garante que logs não vazam segredos nem PII."""
        cfg = load_config()
        prompt_com_pii = "Meu nome é Beto, email beto@gmail.com, tel 11966441212"

        with self.assertLogs("llm_app", level="INFO") as log_capture:
            headers, payload = prepare_request(prompt_com_pii, cfg)

        self.assertEqual(payload["temperature"], 0.3)
        self.assertEqual(payload["max_tokens"], 128)
        self.assertEqual(payload["messages"][0]["content"], "Sistema customizado")
        self.assertIn("Bearer segredo-super-sensivel", headers["Authorization"])

        logs_texto = "\n".join(log_capture.output)
        self.assertNotIn("segredo-super-sensivel", logs_texto)
        self.assertNotIn("beto@gmail.com", logs_texto)
        self.assertNotIn("11966441212", logs_texto)

    def test_input_validation_rejects_blank(self):
        """Valida rejeição de entrada vazia sem acionar rede."""
        with patch("builtins.input", return_value="   "):
            with self.assertRaises(InputValidationError):
                capture_input()

    def test_parse_simulated_valid_response(self):
        """Valida extração de texto a partir de resposta simulada."""
        simulated = {"choices": [{"message": {"content": "  Resposta validada  "}}]}
        self.assertEqual(parse_response(simulated), "Resposta validada")


if __name__ == "__main__":
    unittest.main()