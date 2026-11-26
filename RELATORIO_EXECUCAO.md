INSTITUTO HARDWARE BR

Relatório de Execução — Projeto P0 (Nível Avançado)

Autor: Roberto Regis de Oliveira
Projeto: Extrator de Informações de Contato e Integração com LLM (Ollama)
Versão Entregue: p0-avancado
Ambiente Validado: Windows | Python 3.13 | Modelo qwen2.5:1.5b (Ollama local)


Vídeo de apresentação do P0
https://www.youtube.com/watch?v=vCrCTFnfNIk

< https://github.com/AtiDesign/p0_avancado >
< https://github.com/AtiDesign/p0_avancado/blob/main/README.md >
< https://github.com/AtiDesign/p0_avancado/releases/tag/vv01 >
< https://github.com/AtiDesign/p0_intermediario_rev01 >
< https://github.com/AtiDesign/p0_Basico >




1 - Resumo do P0-Básico
1.1 - Objetivo
Desenvolver uma aplicação em Python capaz de extrair automaticamente informações de contato presentes em textos livres.
1.2 - Problema Escolhido
Extrair:
•	E-mails
•	Telefones
•	URLs
a partir de textos fornecidos pelo usuário.
1.3 - Público-Alvo
Pessoas e pequenas organizações que precisam localizar rapidamente informações de contato em mensagens, documentos, anúncios ou anotações.
1.4 - Tecnologias Utilizadas
•	Python
•	Tkinter (interface gráfica)
•	Expressões Regulares (Regex)
•	Pytest (testes automatizados)
•	Git/GitHub
1.5 - Funcionamento
a)	O usuário insere um texto.
b)	O sistema aplica expressões regulares.
c)	São identificados: 
o	e-mails;
o	telefones;
o	URLs.
d)	Os resultados são exibidos ao usuário.
1.6 - Exemplo
Entrada:
Meu e-mail é joao@email.com.
Meu telefone é (12) 99999-8888.
Visite www.exemplo.com.
Saída:
Plain Text
E-MAILS
------------------------------
joao@email.com
 
TELEFONES
------------------------------
(12) 99999-8888
 
URLS
------------------------------
www.exemplo.com
1.7 - Justificativa para Não Utilizar LLM
Nesta etapa inicial, optou-se por não utilizar um Modelo de Linguagem (LLM), pois o problema escolhido pode ser resolvido de forma eficiente através de regras determinísticas, como opção dada no vídeo de explicação da Hardware.
E-mails, telefones e URLs seguem padrões sintáticos conhecidos, permitindo o uso de Expressões Regulares (Regex), uma solução mais simples, rápida e de menor custo computacional.
O uso de um LLM nesta fase adicionaria complexidade sem trazer benefícios significativos para a resolução do problema.
1.8 - Estrutura do Projeto
p0_basico/
│
├── main.py
├── tests/
│ └── test_extracao.py
├── requirements.txt
├── README.md
└── .gitignore
1.9 - Testes Realizados
Foram criados testes automatizados para verificar:
•	extração correta de e-mails;
•	extração correta de telefones;
•	extração correta de URLs;
•	comportamento quando não existem informações de contato.
Resultado:
collected 4 items

tests/test_extracao.py .... [100%]

4 passed
1.10 - Limitações
•	Não identifica formatos incomuns de telefone.
•	Não valida se o e-mail ou telefone realmente existe.
•	Não interpreta informações escritas de forma indireta.
•	Não utiliza compreensão semântica do texto.
1.11 - Resultado Obtido
Foi desenvolvida uma aplicação funcional capaz de extrair informações de contato de textos livres utilizando Python e Expressões Regulares, com interface gráfica em Tkinter e testes automatizados validados com sucesso. O projeto serviu como base para a evolução do P0-Intermediário, que passou a incorporar integração com um Modelo de Linguagem (LLM) e tratamento avançado de erros.
2 - Resumo do P0-Intermediário
2.1 - Objetivo
Evoluir a aplicação de extração de contatos para integrar um Modelo de Linguagem (LLM) local via API HTTP compatível com OpenAI, substituindo as regras rígidas por compreensão semântica e adicionando arquitetura modular, variáveis de ambiente e tratamento robusto de falhas.
2.2 - Problema Escolhido
Superar as limitações das expressões regulares (Regex) para extrair de textos livres e não padronizados:
•	Nomes (identificados pelo contexto semântico da frase, inviável apenas com Regex);
•	E-mails;
•	Telefones (em diferentes formatos e variações);
•	URLs.
2.3 - Público-Alvo
Profissionais de atendimento, triagem comercial, suporte e pequenas organizações que recebem mensagens desestruturadas (e-mails, chats, formulários ou anotações) e precisam padronizar contatos rapidamente sem depender de serviços externos pagos na nuvem.
2.4 - Tecnologias Utilizadas
•	Python
•	Ollama (execução local do modelo qwen2.5:1.5b via endpoint /v1/chat/completions)
•	Requests (comunicação HTTP e controle de timeout)
•	Python-dotenv (gerenciamento de credenciais e configurações via .env)
•	Tkinter e Threading (interface gráfica responsiva sem congelamento durante a chamada ao modelo)
•	Unittest e Unittest.mock (testes automatizados de cenários de falha simulados)
•	Git / GitHub
2.5 - Funcionamento
1.	O usuário insere um texto livre na interface gráfica (gui.py) ou no terminal (main.py).
2.	O sistema valida a entrada (InputValidationError) e carrega as configurações externas do arquivo .env (config.py).
3.	Uma thread secundária dispara a requisição HTTP (llm_client.py) para o servidor local do Ollama contendo a instrução de extração e o texto do usuário.
4.	O modelo interpreta o contexto e devolve os dados estruturados por categoria (NOMES, E-MAILS, TELEFONES e URLS).
5.	Em caso de falha (servidor offline, credencial inválida, timeout ou resposta malformada), exceções personalizadas (exceptions.py) exibem um aviso amigável ao usuário.
2.6 - Exemplo
Entrada:
meu nome é beto, meu email é beto@gmail.com, meu telefone é 011966441212
Saída:
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
2.7 - Justificativa para Utilizar LLM
Nesta etapa intermediária, a adoção de um LLM tornou-se necessária porque a extração passou a incluir nomes próprios e textos escritos em linguagem natural sem formatação fixa — cenários em que expressões regulares falham ou geram muitos falsos positivos. Com o LLM rodando localmente via Ollama, obteve-se compreensão semântica do texto mantendo privacidade dos dados e custo zero de API.
2.8 - Estrutura do Projeto
p0_intermediario/
│
├── src/
│   ├── config.py
│   ├── exceptions.py
│   ├── llm_client.py
│   ├── main.py
│   └── gui.py
├── tests/
│   └── test_errors.py
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
2.9 - Testes Realizados
Foram implementados testes automatizados com unittest.mock para validar o comportamento da aplicação diante de falhas previsíveis sem depender da rede:
•	Credencial ausente no ambiente (ConfigError);
•	Retorno HTTP 401 — credencial inválida (LLMAuthError);
•	Indisponibilidade do servidor — HTTP 503 (LLMConnectionError);
•	Estouro de tempo limite — Timeout (LLMConnectionError);
•	Resposta JSON vazia ou malformada (LLMResponseError).
Resultado:
Ran 5 tests in 0.085s
OK
2.10 - Limitações
•	Parâmetros de geração do modelo (temperatura, limite de tokens e prompt de sistema) ainda acoplados no código-fonte.
•	Ausência de sistema estruturado de registros operacionais (logging) para auditoria e diagnóstico.
•	Processamento unitário de textos sem histórico ou persistência em arquivo/banco de dados.
2.11 - Resultado Obtido
Foi entregue uma aplicação modular e resiliente capaz de extrair contatos (incluindo nomes) por meio de compreensão semântica com LLM local, protegida contra travamentos de interface e falhas de comunicação. Esta versão consolidou a base arquitetural para a evolução ao P0-Avançado, que incorporou parâmetros externos via .env, logging seguro sem dados sensíveis, ampliação dos testes locais e validação em ambiente limpo.
3 - Resumo do P0-Avançado
3.1 - Objetivo
Consolidar a aplicação em uma versão reproduzível, auditável e pronta para produção local, externalizando todos os parâmetros de comportamento do modelo, implementando registros operacionais seguros (logging), ampliando a cobertura de testes sem chamadas reais ao LLM e validando a instalação em ambiente virtual limpo.
3.2 - Problema Escolhido
Eliminar o acoplamento de parâmetros de geração no código-fonte, garantir rastreabilidade técnica sem expor dados sensíveis (chaves, prompts ou dados pessoais) e assegurar que qualquer pessoa consiga instalar, configurar e testar o sistema do zero de forma determinística.
3.3 - Público-Alvo
Profissionais de atendimento, triagem comercial, suporte e equipes técnicas que necessitam de uma ferramenta local e privada para extração padronizada de contatos, com facilidade para ajustar modelo, criatividade e limites de resposta sem alterar o código-fonte.
3.4 - Tecnologias Utilizadas
•	Python 3.13
•	Ollama (execução local do modelo qwen2.5:1.5b via endpoint /v1/chat/completions)
•	Requests (>= 2.31.0) (comunicação HTTP com medição de latência e controle de timeout)
•	Python-dotenv (>= 1.0.0) (externalização de credenciais e parâmetros de geração via .env)
•	Logging (módulo padrão para registros operacionais sanitizados em logs/app.log)
•	Tkinter e Threading (interface gráfica assíncrona com instrução de extração isolada via system_override)
•	Unittest e Unittest.mock (10 testes automatizados de lógica local e cenários de falha simulados)
•	Git / GitHub (controle de versão com tags evolutivas p0-basico, p0-intermediario e p0-avancado)
3.5 - Funcionamento
a)	O usuário insere o texto na interface gráfica (src/gui.py) ou no terminal (src/main.py).
b)	O módulo src/config.py carrega e valida não apenas a URL, chave e modelo, LLM_MAX_TOKENS e LLM_SYSTEM_PROMPT.
c)	O src/llm_client.py monta o payload com os parâmetros externos (aplicando system_override na GUI para manter o layout estruturado de contatos), mede o tempo de resposta e registra métricas técnicas via src/logger.py.
d)	Os eventos operacionais são gravados em logs/app.log sem registrar chaves de API, texto do prompt ou dados pessoais (PII).
e)	Falhas previsíveis são interceptadas por src/exceptions.py e exibidas de forma segura ao usuário.
3.6 - Exemplo
Entrada:
meu nome é beto, meu email é beto@gmail.com, meu telefone é 011966441212
Saída (GUI):
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

Registro Operacional Gerado (logs/app.log):
2026-11-25 15:30:12 | INFO | llm_client | Solicitação preparada | modelo=qwen2.5:1.5b | temperature=0.20 | max_tokens=256 | tamanho_prompt=73 chars
2026-11-25 15:30:15 | INFO | llm_client | Resposta HTTP recebida | status=200 | duracao=2.84s
2026-11-25 15:30:15 | INFO | llm_client | Resposta extraída com sucesso | tamanho_resposta=142 chars
3.7 - Justificativa para a Arquitetura Avançada
Manter um LLM em uso prático exige separação clara entre código e configuração: ao mover temperatura, limite de tokens, prompt de sistema e escolha do modelo para o .env, tornou-se possível substituir o modelo qwen3.5:4b (lento em CPU devido ao modo de raciocínio interno) pelo qwen2.5:1.5b em segundos, sem tocar na lógica da aplicação. Paralelamente, o logging sanitizado e os testes sem chamada real garantem observabilidade e validação rápida sem custo computacional.
3.8 - Estrutura do Projeto
p0_avancado/
│
├── src/
│   ├── config.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── llm_client.py
│   ├── main.py
│   └── gui.py
├── tests/
│   ├── test_errors.py
│   └── test_local_logic.py
├── logs/                  (ignorado no Git)
├── .env                   (ignorado no Git)
├── .env.example
├── requirements.txt
├── README.md
├── RELATORIO_EXECUCAO.md
└── .gitignore
3.9 - Testes Realizados
A suíte foi ampliada para 10 testes automatizados (test_errors.py e test_local_logic.py), executados localmente sem realizar chamadas reais à rede ou ao Ollama:
•	Simulação de falhas: credencial ausente, HTTP 401, HTTP 503, timeout e resposta JSON malformada/vazia;
•	Lógica local e configuração: rejeição de entrada em branco, bloqueio de temperatura fora da faixa (0.0–2.0), carregamento de parâmetros customizados, extração de resposta simulada e auditoria garantindo que logs não vazam credenciais nem PII.
Resultado:
Ran 10 tests in 0.120s

OK
3.10 - Limitações
•	Processa um texto por vez, sem processamento em lote (batch) ou exportação direta para planilhas/CSV.
•	Não possui persistência histórica das extrações em banco de dados.
•	O tempo de resposta permanece condicionado ao hardware local disponível para execução do Ollama.
3.11 - Resultado Obtido
Foi concluída e validada em ambiente virtual limpo (.venv_limpa) uma aplicação completa, modular, segura e reproduzível. A versão final (p0-avancado) reúne interface gráfica e CLI, reconfiguração externa sem alteração de código, auditoria segura de logs, documentação completa (README.md e RELATORIO_EXECUCAO.md) e 100% de aprovação nos testes automatizados.

