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
    if mensagem == "": # Tratamento para caso for pressionado apenas "Enter" no input da mensagem
        mensagem = " "
    client_socket.sendall(mensagem.encode("utf-8")) # Envio da mensagem para o servidor
    resposta = client_socket.recv(1024)
    print(resposta.decode("utf-8")) # Confirmação de recebimento enviada pelo servidor
    client_socket.close() # Encerramento da conexão

# Inicia o cliente TCP
start_client_tcp()