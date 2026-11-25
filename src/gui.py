import threading
import tkinter as tk
from tkinter import scrolledtext

from config import load_config
from exceptions import AppError
from llm_client import call_model, parse_response, prepare_request

INSTRUCAO_EXTRATOR = (
    "Você é um extrator de informações de contato. Extraia do texto fornecido: "
    "NOMES, E-MAILS, TELEFONES e URLS. Responda em português, estritamente neste formato:\n\n"
    "NOMES\n------------------------------\n(lista ou 'Nenhum encontrado')\n\n"
    "E-MAILS\n------------------------------\n(lista ou 'Nenhum encontrado')\n\n"
    "TELEFONES\n------------------------------\n(lista ou 'Nenhum encontrado')\n\n"
    "URLS\n------------------------------\n(lista ou 'Nenhuma encontrada')"
)


def processar_extracao():
    texto = entrada.get("1.0", tk.END).strip()

    if not texto:
        exibir_resultado("[Aviso] Digite ou cole um texto antes de extrair.")
        return

    # Desabilita o botão enquanto o Ollama processa
    botao.config(state=tk.DISABLED, text="Processando no Ollama...")
    exibir_resultado("Aguardando resposta do modelo...")

    def tarefa_llm():
        try:
            config = load_config()
            headers, payload = prepare_request(
                texto, config, system_override=INSTRUCAO_EXTRATOR
            )
            response = call_model(headers, payload, config)
            resposta_formatada = parse_response(response)
            janela.after(0, lambda res=resposta_formatada: exibir_resultado(res))
        except AppError as erro:
            mensagem_erro = f"[Aviso] {erro}"
            janela.after(0, lambda msg=mensagem_erro: exibir_resultado(msg))
        finally:
            janela.after(
                0,
                lambda: botao.config(state=tk.NORMAL, text="Extrair Informações"),
            )

    threading.Thread(target=tarefa_llm, daemon=True).start()


def exibir_resultado(mensagem: str):
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, mensagem)


# Configuração da Janela
janela = tk.Tk()
janela.title("Extrator de Informações com LLM (Ollama)")
janela.geometry("700x520")

titulo = tk.Label(
    janela,
    text="Extrator de Informações de Contato",
    font=("Arial", 14, "bold"),
)
titulo.pack(pady=10)

entrada = scrolledtext.ScrolledText(janela, height=9, font=("Consolas", 10))
entrada.pack(fill="both", padx=10, pady=5)

botao = tk.Button(
    janela,
    text="Extrair Informações",
    font=("Arial", 10, "bold"),
    command=processar_extracao,
)
botao.pack(pady=10)

resultado = scrolledtext.ScrolledText(janela, height=13, font=("Consolas", 10))
resultado.pack(fill="both", padx=10, pady=5)

janela.mainloop()