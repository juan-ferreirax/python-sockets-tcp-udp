# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading
import logging
import os
from datetime import datetime

# Constantes de configuração
HOST = "0.0.0.0"   # Aceita conexões de qualquer interface de rede
PORT = 7000         # Porta em que o servidor irá escutar

# Os logs serão salvos em "servidor.log" e também exibidos no console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(
            __file__), "servidor.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def atender_cliente(conn, addr):
    # Função executada por cada thread para atender um cliente individualmente.

    logging.info(f"Conexão recebida de {addr}")

    try:
        # Aguarda qualquer mensagem do cliente (a "solicitação" de hora)
        dados = conn.recv(1024)

        if dados:
            hora_atual = datetime.now().strftime("%H:%M:%S")

            conn.sendall(hora_atual.encode("utf-8"))

            logging.info(f"Hora enviada para {addr}: {hora_atual}")
        else:
            logging.warning(f"Cliente {addr} conectou mas não enviou dados.")

    except Exception as e:
        # Garante que uma falha em um cliente não derruba o servidor
        logging.error(f"Erro ao atender cliente {addr}: {e}")

    finally:
        conn.close()
        logging.info(f"Conexão encerrada com {addr}")


def iniciar_servidor():
    """
    Função principal que inicializa o servidor TCP e fica
    aguardando conexões de clientes em loop infinito.
    """
    # Cria o socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST, PORT))

        servidor.listen(5)

        logging.info(f"Servidor de hora rodando em {HOST}:{PORT}...")

        while True:
            try:
                conn, addr = servidor.accept()

                thread = threading.Thread(
                    target=atender_cliente,
                    args=(conn, addr),
                    name=f"Thread-{addr[1]}",
                    daemon=True
                )
                thread.start()

            except KeyboardInterrupt:
                logging.info("Servidor encerrado pelo operador (Ctrl+C).")
                break

            except Exception as e:
                logging.error(f"Erro no loop principal do servidor: {e}")


# Ponto de entrada do script
if __name__ == "__main__":
    iniciar_servidor()
