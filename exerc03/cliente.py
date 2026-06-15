# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading
import sys

try:
    ENDERECO_IP = input("Informe o endereço IP do servidor: ")
    PORTA = int(input("Informe a porta do servidor: "))
except KeyboardInterrupt:
    print("\nCliente finalizado.")
    raise SystemExit

PROMPT = "Digite sua mensagem: "


def receber_mensagens(client_socket):
    """
    Thread responsável por receber mensagens do servidor e exibi-las no terminal
    sem sobrescrever o que o usuário está digitando.
    """
    try:
        while True:
            # Bloqueia aguardando dados do servidor 
            data = client_socket.recv(1024)

            # recv() retorna bytes vazios quando o servidor fecha a conexão
            if not data:
                sys.stdout.write("\nConexão encerrada pelo servidor.\n")
                sys.stdout.flush()
                break

            mensagem = data.decode("utf-8", errors="replace")

            # Sequência para evitar sobreposição com o que o usuário está digitando:
            # \r           → move o cursor para o início da linha atual
            # ' ' * 80     → sobrescreve a linha inteira com espaços (apaga o prompt residual)
            # \r           → volta ao início da linha de novo
            # {mensagem}\n → imprime a mensagem recebida e quebra a linha
            # {PROMPT}     → reexibe o prompt limpo para o usuário continuar digitando
            sys.stdout.write(f"\r{' ' * 80}\r{mensagem}\n{PROMPT}")

            # flush() força a escrita imediata no terminal,
            # necessário pois sys.stdout usa buffer por padrão
            sys.stdout.flush()

    except OSError:
        # OSError ocorre quando o socket é fechado pela thread de envio
        pass


def enviar_mensagens(client_socket):
    """
    Thread responsável por capturar a entrada do usuário e enviar ao servidor.
    """
    try:
        while True:
            # input() sem argumento evita duplicar o prompt,
            # pois ele já é exibido pelo main() e pela thread de recebimento
            mensagem = input().strip()

            if mensagem == "":
                sys.stdout.write(f"Erro: mensagem vazia.\n{PROMPT}")
                sys.stdout.flush()
                continue

            # Codifica em UTF-8 antes de enviar pelo socket (que trabalha com bytes)
            client_socket.send(mensagem.encode("utf-8"))

            # Verifica o comando de saída somente após enviar,
            # para que o outro cliente receba o aviso de desconexão
            if mensagem.lower() == "sair":
                sys.stdout.write("Encerrando cliente...\n")
                sys.stdout.flush()
                break

    except OSError as erro:
        sys.stdout.write(f"Erro ao enviar: {erro}\n")
        sys.stdout.flush()

    finally:
        # Garante que o socket seja fechado mesmo se ocorrer uma exceção,
        # o que também interrompe o recv() bloqueante da thread de recebimento
        client_socket.close()


def main():
    # AF_INET = protocolo IPv4 | SOCK_STREAM = conexão TCP orientada a fluxo
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ENDERECO_IP, PORTA))
        print("Conectado ao servidor de chat.")
        print("Digite 'sair' para encerrar.\n")

        # Exibe o prompt uma única vez antes das threads iniciarem,
        # evitando duplicação já que input() na thread de envio não tem argumento
        sys.stdout.write(PROMPT)
        sys.stdout.flush()

        # daemon=True faz a thread de recebimento encerrar automaticamente
        # quando a thread principal terminar
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

        # Aguarda a thread de envio terminar 
        thread_enviar.join()

    except ConnectionRefusedError:
        print("Erro: não foi possível conectar ao servidor.")
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    except OSError as erro:
        print(f"Erro no cliente: {erro}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()