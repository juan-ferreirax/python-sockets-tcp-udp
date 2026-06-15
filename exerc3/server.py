# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading

def encaminhar_mensagens(cliente_origem, cliente_destino, nome_cliente):
    """
    Recebe mensagens de um cliente e encaminha para o outro.
    """
    try:
        while True:
            data = cliente_origem.recv(1024)

            if not data:
                break

            mensagem = data.decode("utf-8", errors="replace").strip()

            if mensagem.lower() == "sair":
                aviso = f"{nome_cliente} saiu do chat."
                cliente_destino.send(aviso.encode("utf-8"))
                break

            print(f"{nome_cliente}: {mensagem}")

            mensagem_encaminhada = f"{nome_cliente}: {mensagem}"
            cliente_destino.send(mensagem_encaminhada.encode("utf-8"))

    except OSError as erro:
        print(f"Erro na comunicação com {nome_cliente}: {erro}")

    finally:
        cliente_origem.close()
        cliente_destino.close()
        print(f"Conexão com {nome_cliente} encerrada.")


def main():
    host = "127.0.0.1"
    port = 7001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar a porta caso o servidor seja reiniciado rapidamente
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(2)

        print(f"Servidor de chat ouvindo em {host}:{port}...")
        print("Aguardando dois clientes se conectarem...")

        cliente1, endereco1 = server_socket.accept()
        print(f"Cliente 1 conectado: {endereco1}")
        cliente1.send("Você é o Cliente 1. Aguardando o Cliente 2...".encode("utf-8"))

        cliente2, endereco2 = server_socket.accept()
        print(f"Cliente 2 conectado: {endereco2}")

        cliente1.send("Cliente 2 conectado. Chat iniciado.".encode("utf-8"))
        cliente2.send("Você é o Cliente 2. Chat iniciado.".encode("utf-8"))

        # Uma thread encaminha mensagens do cliente 1 para o cliente 2
        thread1 = threading.Thread(
            target=encaminhar_mensagens,
            args=(cliente1, cliente2, "Cliente 1")
        )

        # Outra thread encaminha mensagens do cliente 2 para o cliente 1
        thread2 = threading.Thread(
            target=encaminhar_mensagens,
            args=(cliente2, cliente1, "Cliente 2")
        )

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")

    except OSError as erro:
        print(f"Erro no servidor: {erro}")

    finally:
        server_socket.close()
        print("Servidor finalizado.")


if __name__ == "__main__":
    main()