# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket

def main():
    host = "127.0.0.1"
    port = 6000

    #Tamanho máximo aproximado permitido para uma mensagem UDP em IPv4
    max_size = 65507

    #Cria socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server_socket.bind((host,port))
        print(f"Servidor UDP ouvindo em {host}:{port}...")

        while True:
            try:
                # Recebe a mensagem e o endereço do cliente
                data, client_address = server_socket.recvfrom(max_size)

                message = data.decode("utf-8", errors="replace")
                print(f"Mensagem recebida de {client_address}: {message}")

                # Envia a mesma mensagem de volta para o cliente
                server_socket.sendto(data, client_address)

            except OSError as error:
                print(f"Erro de comunicação no servidor: {error}")

    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")

    except OSError as error:
        print(f"Erro ao iniciar o servidor: {error}")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()   