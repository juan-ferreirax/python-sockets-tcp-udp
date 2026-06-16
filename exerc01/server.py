# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading

try:
    ENDERECO_IP = input("Informe o endereço IP do servidor: ")
    PORTA = int(input("Informe uma porta(0 para o SO escolher automaticamente): "))
except KeyboardInterrupt:
    print("\nServidor finalizado.")
    raise SystemExit

def gerenciar_cliente(conexao, endereco):
    # Tratamento de excessão
    try:
        data = conexao.recv(1024).decode("utf-8") # Recebimento dos dados do cliente
        
        # Validação de mensagem vazia
        if not data or not data.strip():
            print(f"O cliente [{endereco[1]}] Enviou uma mensagem vazia.")
            conexao.sendall("Erro: Mensagem vazia não permitida.".encode("utf-8"))
        else:
            print(f"[{endereco[1]}] Mensagem: {data}")
            conexao.sendall("Mensagem recebida pelo servidor!".encode("utf-8"))
    except Exception as e:
        print(f"Erro na conexão com {endereco[1]}: {e}")
    finally:
        conexao.close()

def start_servidor_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket TCP
    server_socket.bind((ENDERECO_IP, PORTA)) # Faz associação de IP e Porta
    server_socket.listen()
    if PORTA == 0:
        porta_real = server_socket.getsockname()[1]
    else:
        porta_real = PORTA
    print(f"Servidor ouvindo em {ENDERECO_IP}:{porta_real}...")

    # Loop para permitir multiplas conexões de clientes
    while True:
        conexao, endereco = server_socket.accept()
        print(f"Conexão estabelecida com {endereco[0]}:{endereco[1]}! Aguardando mensagem...")
        thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco))
        thread.start()

# Inicia o servidor TCP
start_servidor_tcp()