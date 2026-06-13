# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket

ENDERECO_IP = "127.0.0.1"
PORTA = 8000

def start_servidor_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket TCP
    server_socket.bind((ENDERECO_IP, PORTA)) # Faz associação de IP e Porta
    server_socket.listen()
    print(f"Servidor ouvindo na porta {PORTA}...")

    connection, address = server_socket.accept()
    print("Conexão estabelecida com sucesso! Aguardando mensagem...")

    data = connection.recv(1024).decode("utf-8")
    connection.sendall("Mensagem recebida pelo servidor!".encode("utf-8"))
    print(data)

    server_socket.close()

# Inicia o servidor TCP
start_servidor_tcp()