# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket

ENDERECO_IP = "127.0.0.1"
PORTA = 8000

def start_client_tcp():
    # Cria o socket TCP e realiza a conexão com o servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ENDERECO_IP, PORTA))
    print("Conexão estabelecida com sucesso!")

    mensagem = input("Digite sua mensagem: ")
    if mensagem == "":
        mensagem = " "
    client_socket.sendall(mensagem.encode("utf-8"))
    resposta = client_socket.recv(1024)
    print(resposta.decode("utf-8"))
    client_socket.close()

# Inicia o cliente TCP
start_client_tcp()