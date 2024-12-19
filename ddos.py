import requests
from threading import Thread
import random
import time
import tkinter as tk

# Configurações
URLS = [
    "http://192.168.1.80:8000/",
    "http://192.168.1.80:8000/api/test",
    "http://192.168.1.80:8000/login",
]  # Diferentes endpoints para alternar
NUM_THREADS = 100  # Reduzi o número de threads para simplificar
RUNNING = True  # Controle de execução
REQUESTS_LIMIT = 500  # Limite de requisições por thread

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/91.0"},
    {"User-Agent": "Safari/537.36"},
]  # Cabeçalhos customizados para tráfego variado

# Função para exibir uma animação visual impactante
def display_animation(progress_text_widget):
    """Exibe uma animação de ataque cibernético durante a execução"""
    chars = ['.', 'o', 'O', '@', '#', '%', '&']

    def insert_animation():
        for char in chars:
            if RUNNING:
                progress_text_widget.insert(tk.END, f"Ataque em andamento {char} \n")
                progress_text_widget.yview(tk.END)  # Rola a tela para o fim
            time.sleep(0.1)  # Animação mais rápida
        if RUNNING:  # Re-inicia a animação periodicamente
            progress_text_widget.after(100, insert_animation)

    insert_animation()  # Inicia a animação

# Função que envia requisições contínuas e variadas
def send_requests(progress_text_widget):
    """Função que envia requisições contínuas e variadas."""
    def send():
        count = 0
        while RUNNING and count < REQUESTS_LIMIT:
            try:
                url = random.choice(URLS)  # Escolhe um endpoint aleatório
                headers = random.choice(HEADERS_LIST)  # Escolhe um cabeçalho aleatório
                method = random.choice(["GET", "POST"])  # Alterna entre métodos HTTP

                if method == "GET":
                    response = requests.get(url, headers=headers, timeout=0.5)
                elif method == "POST":
                    response = requests.post(url, headers=headers, data={"key": "value"}, timeout=0.5)

                # Envia a atualização de logs para a thread principal
                progress_text_widget.after(
                    0,
                    lambda method=method, url=url, response=response, headers=headers:
                    progress_text_widget.insert(
                        tk.END, f"{method} para {url} - Status: {response.status_code} - Header: {headers}\n"
                    ),
                )
                progress_text_widget.yview(tk.END)  # Rola a tela para o fim
                count += 1
                time.sleep(0.001)  # Intervalo reduzido entre requisições

            except Exception as e:
                # Envia erros para a thread principal
                progress_text_widget.after(
                    0,
                    lambda e=e: progress_text_widget.insert(tk.END, f"Erro: {e}\n")
                )
                progress_text_widget.yview(tk.END)  # Rola a tela para o fim
                time.sleep(0.01)

        progress_text_widget.after(
            0, lambda: progress_text_widget.insert(tk.END, "Thread finalizada.\n")
        )
        progress_text_widget.yview(tk.END)

    send()  # Inicia o envio de requisições

# Função para inicializar a interface
def create_gui():
    """Cria a interface gráfica do teste."""
    # Cria a janela principal
    window = tk.Tk()
    window.title("Teste de Carga - Sala de Aula")
    window.geometry("800x600")  # Tamanho da janela
    window.configure(bg="black")  # Fundo preto

    # Cria o widget de texto para exibir a animação
    progress_text_widget = tk.Text(window, bg="black", fg="green", font=("Courier", 12), height=30, width=90)
    progress_text_widget.pack()

    # Inicia as threads de requisições
    threads = []
    for i in range(NUM_THREADS): 300
    thread = Thread(target=send_requests, args=(progress_text_widget,), daemon=True)
    threads.append(thread)
    thread.start()

    # Inicia a animação visual
    animation_thread = Thread(target=display_animation, args=(progress_text_widget,), daemon=True)
    animation_thread.start()

    # Exibe a janela
    window.mainloop()

# Inicia a execução
if __name__ == "__main__":
    print("Iniciando teste de carga...")
    create_gui()
