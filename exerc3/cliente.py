# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading

def receber_mensagens(client_socket):
    """
    Thread responsável por receber mensagens do servidor.
    """
    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                print("\nConexão encerrada pelo servidor.")
                break

            mensagem = data.decode("utf-8", errors="replace")
            print(f"\n{mensagem}")
            print("Digite sua mensagem: ", end="")

    except OSError:
        print("\nRecebimento de mensagens encerrado.")


def enviar_mensagens(client_socket):
    """
    Thread responsável por enviar mensagens para o servidor.
    """
    try:
        while True:
            mensagem = input("Digite sua mensagem: ").strip()

            if mensagem == "":
                print("Erro: a mensagem não pode estar vazia.")
                continue

            client_socket.send(mensagem.encode("utf-8"))

            if mensagem.lower() == "sair":
                print("Encerrando cliente...")
                break

    except OSError as erro:
        print(f"Erro ao enviar mensagem: {erro}")

    finally:
        client_socket.close()


def main():
    host = "127.0.0.1"
    port = 7001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("Conectado ao servidor de chat.")
        print("Digite 'sair' para encerrar.\n")

        thread_receber = threading.Thread(
            target=receber_mensagens,
            args=(client_socket,),
            daemon=True
        )

        thread_enviar = threading.Thread(
            target=enviar_mensagens,
            args=(client_socket,)
        )

        thread_receber.start()
        thread_enviar.start()

        thread_enviar.join()

    except ConnectionRefusedError:
        print("Erro: não foi possível conectar ao servidor. Verifique se o servidor está ligado.")

    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")

    except OSError as erro:
        print(f"Erro no cliente: {erro}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()