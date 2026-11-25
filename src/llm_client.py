import time
import requests
from config import AppConfig
from exceptions import LLMAuthError, LLMConnectionError, LLMResponseError
from logger import get_logger

logger = get_logger()


def prepare_request(
    prompt: str, config: AppConfig, system_override: str | None = None
) -> tuple[dict, dict]:
    """Prepara cabeçalhos e corpo da solicitação usando parâmetros externos."""
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    system_message = system_override if system_override is not None else config.system_prompt
    payload = {
        "model": config.model_name,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
    }
    logger.info(
        "Solicitação preparada | modelo=%s | temperature=%.2f | max_tokens=%d | tamanho_prompt=%d chars",
        config.model_name,
        config.temperature,
        config.max_tokens,
        len(prompt),
    )
    return headers, payload


def call_model(headers: dict, payload: dict, config: AppConfig) -> dict:
    """Executa a chamada HTTP ao LLM com medição de tempo e logs sem dados sensíveis."""
    inicio = time.perf_counter()
    try:
        response = requests.post(
            config.api_url,
            headers=headers,
            json=payload,
            timeout=config.timeout,
        )
    except requests.exceptions.Timeout as exc:
        logger.warning("Timeout após %ss ao consultar modelo=%s", config.timeout, config.model_name)
        raise LLMConnectionError(
            f"O serviço demorou mais de {config.timeout}s para responder (Timeout). Tente novamente mais tarde."
        ) from exc
    except requests.exceptions.RequestException as exc:
        logger.error("Falha de conexão com o endpoint configurado.")
        raise LLMConnectionError(
            "Não foi possível conectar ao serviço de LLM. Verifique a URL e se o servidor está ativo."
        ) from exc

    duracao = time.perf_counter() - inicio
    logger.info("Resposta HTTP recebida | status=%d | duracao=%.2fs", response.status_code, duracao)

    if response.status_code in (401, 403):
        logger.warning("Falha de autenticação HTTP %d", response.status_code)
        raise LLMAuthError("Falha de autenticação: verifique sua LLM_API_KEY no arquivo .env.")
    if response.status_code >= 500:
        logger.error("Indisponibilidade remota HTTP %d", response.status_code)
        raise LLMConnectionError(
            f"O serviço externo está temporariamente indisponível (Código HTTP {response.status_code})."
        )
    if response.status_code >= 400:
        logger.warning("Solicitação recusada HTTP %d", response.status_code)
        raise LLMResponseError(
            f"O serviço recusou a solicitação (Código HTTP {response.status_code}). Verifique os parâmetros do modelo."
        )

    try:
        return response.json()
    except ValueError as exc:
        logger.error("Corpo da resposta não é um JSON válido.")
        raise LLMResponseError("A resposta recebida do servidor não está em formato JSON válido.") from exc


def parse_response(data: dict) -> str:
    """Extrai o texto final da resposta sem registrar conteúdo sensível em log."""
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        logger.error("Estrutura JSON inesperada na resposta do modelo.")
        raise LLMResponseError("A resposta do modelo veio em um formato inesperado ou incompleto.") from exc

    if not isinstance(content, str) or not content.strip():
        logger.warning("Modelo retornou conteúdo vazio.")
        raise LLMResponseError("O modelo retornou uma resposta vazia.")

    logger.info("Resposta extraída com sucesso | tamanho_resposta=%d chars", len(content))
    return content.strip()