# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket

def main():
    host = "127.0.0.1"
    port = 6000

    # Tamanho máximo aproximado permitido para uma mensagem UDP em IPv4
    max_size = 65507

    # Cria o socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define tempo limite para esperar resposta do servidor
    client_socket.settimeout(5)

    print("Cliente UDP iniciado.")
    print("Digite uma mensagem ou 'sair' para encerrar.")

    try:
        while True:
            message = input("Mensagem: ").strip()

            if message.lower() == "sair":
                print("Cliente encerrado.")
                break

            if message == "":
                print("Erro: a mensagem não pode estar vazia.")
                continue

            message_bytes = message.encode("utf-8")

            # Validação do tamanho máximo da mensagem
            if len(message_bytes) > max_size:
                print(f"Erro: a mensagem excede o limite de {max_size} bytes.")
                continue

            try:
                # Envia a mensagem para o servidor
                client_socket.sendto(message_bytes, (host, port))

                # Aguarda a resposta do servidor
                data, server_address = client_socket.recvfrom(max_size)

                response = data.decode("utf-8", errors="replace")
                print(f"Eco recebido de {server_address}: {response}")

            except socket.timeout:
                print("Erro: tempo limite excedido. O pacote pode ter sido perdido ou o servidor pode estar desligado.")

            except OSError as error:
                print(f"Erro de comunicação no cliente: {error}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
