# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales
import socket

# Configurações de conexão
try:
    HOST = input("Informe o endereço IP do servidor: ")
    PORT = int(input("Informe a porta do servidor: "))
except KeyboardInterrupt:
    print("\nCliente finalizado.")
    raise SystemExit

def solicitar_hora():
    try:
        # Cria o socket TCP e conecta ao servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            print(f"Conectado ao servidor {HOST}:{PORT}")

            # Envia uma solicitação ao servidor
            cliente.sendall("HORA".encode("utf-8"))

            resposta = cliente.recv(1024).decode("utf-8")

            if resposta:
                print(f"Hora recebida do servidor: {resposta}")
            else:
                print("Nenhuma resposta recebida do servidor.")

    except ConnectionRefusedError:
        # Ocorre quando o servidor não está rodando ou a porta está errada
        print(
            f"Erro: Não foi possível conectar ao servidor em {HOST}:{PORT}. Verifique se o servidor está rodando.")

    except Exception as e:
        print(f"Erro inesperado: {e}")


# Ponto de entrada do script
if __name__ == "__main__":
    solicitar_hora()
