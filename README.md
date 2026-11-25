# p0_avancado
Extrair e-mails, telefones e URLs de um texto

# Integração com LLM — Nível Avançado (Entrega Reproduzível)

Aplicação desenvolvida em Python para interação com Modelos de Linguagem (LLMs), evoluída para o **Nível Avançado** com foco em reprodutibilidade, configuração externa de parâmetros de geração, registros operacionais seguros (*logging*), cobertura de testes locais e validação em ambiente limpo.

---

## Ambiente e Versões Utilizadas

* **Linguagem:** Python 3.13 (compatível com Python 3.11+)
* **Bibliotecas Externas (`requirements.txt`):**
  * `requests >= 2.31.0` — Comunicação HTTP com o endpoint do LLM.
  * `python-dotenv >= 1.0.0` — Carregamento de variáveis de ambiente a partir do `.env`.
* **Bibliotecas Padrão Utilizadas:**
  * `tkinter` — Interface gráfica desktop.
  * `logging` — Registros operacionais sem dados sensíveis.
  * `unittest` e `unittest.mock` — Suíte de testes automatizados locais e simulados.

---

## Arquitetura e Organização do Código

O projeto mantém uma arquitetura modular dentro de `src/` e uma suíte de testes em `tests/`:

* **`src/config.py`**: Carrega e valida as variáveis de ambiente do arquivo `.env`, incluindo credenciais de acesso (`LLM_API_URL`, `LLM_API_KEY`, `LLM_MODEL_NAME`, `LLM_TIMEOUT`) e parâmetros externos de comportamento (`LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `LLM_SYSTEM_PROMPT`).
* **`src/exceptions.py`**: Define exceções específicas (`AppError`, `ConfigError`, `InputValidationError`, `LLMAuthError`, `LLMConnectionError`, `LLMResponseError`) para converter falhas técnicas em mensagens controladas ao usuário.
* **`src/logger.py`**: Configura o registro operacional em `logs/app.log`, gravando métricas técnicas (modelo, parâmetros numéricos, status HTTP, latência e tamanho em caracteres) sem armazenar chaves, tokens, prompts ou dados pessoais (PII).
* **`src/llm_client.py`**: Prepara cabeçalhos e *payload* com os parâmetros configurados externamente (`prepare_request`), executa a chamada HTTP com controle de timeout (`call_model`) e valida a resposta (`parse_response`).
* **`src/main.py`**: Interface via linha de comando (CLI) que captura e valida a entrada do usuário, consulta o modelo e exibe a resposta tratada.
* **`src/gui.py`**: Interface gráfica desktop em `tkinter` para extração estruturada de contatos (nomes, e-mails, telefones e URLs) com execução assíncrona via *threads*.
* **`tests/test_errors.py` e `tests/test_local_logic.py`**: Testes automatizados da lógica local e de cenários de falha simulados, executáveis sem realizar chamadas reais ao LLM.

---

## Pré-requisitos e Instalação

1. **Clone o repositório e acesse a pasta do projeto:**
   ```bash
   git clone [https://github.com/AtiDesign/p0_avancado.git](https://github.com/AtiDesign/p0_avancado.git)
   cd p0_avancado

2. **Crie e ative o ambiente virtual (.venv):**
    Windows (PowerShell):
        PowerShell
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1

    Linux / macOS:
        Bash
        python3 -m venv .venv
        source .venv/bin/activate

3. **Instale as dependências:**
    pip install -r requirements.txt

4. **Instale o Ollama e baixe o modelo leve recomendado:**
    ollama pull qwen2.5:1.5b

5. **Crie o arquivo .env a partir do .env.example:**
    Windows (PowerShell):
    PowerShell
    Copy-Item .env.example .env

    Linux / macOS:
    Bash
    cp .env.example .env

6. **Configure o arquivo .env na raiz do projeto:**
    LLM_API_URL=http://localhost:11434/v1/chat/completions
    LLM_API_KEY=ollama
    LLM_MODEL_NAME=qwen2.5:1.5b
    LLM_TIMEOUT=60

    # Parâmetros de geração e comportamento
    LLM_TEMPERATURE=0.2
    LLM_MAX_TOKENS=256
    LLM_SYSTEM_PROMPT=Você é um assistente objetivo e claro. Responda em português.
    
    ## Segurança: Os diretórios/arquivos .env e logs/ estão listados no .gitignore para evitar o versionamento de segredos ou registros locais.

7. **Como Executar:**
    Execução via Terminal (CLI)
    PowerShell
    python src\main.py
    Execução via Interface Gráfica (GUI)
    PowerShell
    python src\gui.py

8. **Execução dos Testes Automatizados (Sem chamada real ao LLM)**
    PowerShell
    python -m unittest discover tests -v

9. **Exemplos de Entrada, Saída e Logs**
    Extração estruturada via Interface Gráfica (src/gui.py)
        Entrada:

            Exemplo;
            meu nome é joão, meu email é joão@gmail.com, meu telefone é 011966441212
        
        Saída:

            Exemplo;
            NOMES
            ------------------------------
            beto

            E-MAILS
            ------------------------------
            beto@gmail.com

            TELEFONES
            ------------------------------
            011966441212

            URLS
            ------------------------------
            Nenhuma encontrada
        
        Registro operacional seguro (logs/app.log):
            
            2026-11-25 15:30:12 | INFO | llm_client | Solicitação preparada | modelo=qwen2.5:1.5b | temperature=0.20 | max_tokens=256 | tamanho_prompt=73 chars
            2026-11-25 15:30:15 | INFO | llm_client | Resposta HTTP recebida | status=200 | duracao=2.84s
            2026-11-25 15:30:15 | INFO | llm_client | Resposta extraída com sucesso | tamanho_resposta=142 chars

10. **Execução da suíte de testes (unittest)**
        test_empty_or_malformed_response (test_errors.TestLLMErrorHandling.test_empty_or_malformed_response) ... ok
        test_invalid_credential (test_errors.TestLLMErrorHandling.test_invalid_credential) ... ok
        test_missing_credential (test_errors.TestLLMErrorHandling.test_missing_credential) ... ok
        test_service_unavailable (test_errors.TestLLMErrorHandling.test_service_unavailable) ... ok
        test_timeout (test_errors.TestLLMErrorHandling.test_timeout) ... ok
        test_input_validation_rejects_blank (test_local_logic.TestLocalLogic.test_input_validation_rejects_blank) ... ok
        test_invalid_temperature_raises_config_error (test_local_logic.TestLocalLogic.test_invalid_temperature_raises_config_error) ... ok
        test_load_custom_generation_parameters (test_local_logic.TestLocalLogic.test_load_custom_generation_parameters) ... ok
        test_parse_simulated_valid_response (test_local_logic.TestLocalLogic.test_parse_simulated_valid_response) ... ok
        test_prepare_request_and_safe_logging (test_local_logic.TestLocalLogic.test_prepare_request_and_safe_logging) ... ok

        ----------------------------------------------------------------------
        Ran 10 tests in 0.120s

        OK

11. **Relatório de Validação em Ambiente Limpo**
    A entrega final foi validada em um ambiente virtual limpo (.venv_limpa), criado do zero no Windows com Python 3.13, seguindo exclusivamente as instruções deste README.md:

    Instalação de dependências: pip install -r requirements.txt concluído sem erros.

    Testes automatizados: python -m unittest discover tests -v aprovou todos os 10 testes locais e simulados (OK).

    Execução real (CLI e GUI): Tanto src/main.py quanto src/gui.py executaram corretamente com o Ollama local utilizando os parâmetros externos do .env.

    Auditoria de registros (logs/app.log): Confirmado que apenas dados técnicos (modelo, parâmetros numéricos, status HTTP, duração e contagem de caracteres) são gravados, sem exposição de chaves ou dados pessoais.

    Problemas encontrados e correções aplicadas durante a validação:

        1. Escopo de exceção assíncrona no src/gui.py: Ao exibir mensagens de erro dentro do callback janela.after do tkinter, ocorria NameError porque o Python limpa a variável do bloco except ao sair do escopo. Corrigido vinculando a mensagem diretamente como parâmetro padrão na lambda (lambda msg=mensagem_erro: exibir_resultado(msg)).

        2. Compatibilidade dos testes legados (tests/test_errors.py): Após a inclusão dos novos campos obrigatórios em AppConfig (temperature, max_tokens, system_prompt), o setUp dos testes anteriores falhou por falta desses argumentos. Corrigido definindo valores padrão na dataclass AppConfig e atualizando o setUp e as asserções de mensagens em tests/test_errors.py.

        3. Desempenho e tempo de resposta do modelo local: O modelo qwen3.5:4b apresentava latência elevada em CPU devido ao modo de raciocínio interno (thinking). O .env e o .env.example foram reconfigurados para o modelo leve qwen2.5:1.5b com LLM_MAX_TOKENS=256, reduzindo o tempo de resposta para poucos segundos sem alterar o núcleo da aplicação.