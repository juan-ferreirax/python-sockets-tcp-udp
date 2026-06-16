# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import socket
import threading

try:
    ENDERECO_IP = input("Informe o endereço IP do servidor: ")
    PORTA = int(input("Informe a porta do servidor: "))
except KeyboardInterrupt:
    print("\nServidor finalizado.")
    raise SystemExit


def encaminhar_mensagens(cliente_origem, cliente_destino, nome_cliente):
    """
    Recebe mensagens de um cliente e encaminha para o outro.
    Executada em thread separada para cada direção da comunicação.
    """
    try:
        while True:
            # Bloqueia aguardando dados do cliente de origem (até 1024 bytes por vez)
            data = cliente_origem.recv(1024)

            # recv() retorna bytes vazios quando o cliente fecha a conexão
            if not data:
                break

            mensagem = data.decode("utf-8", errors="replace").strip()

            # Detecta o comando de saída antes de encaminhar,
            # para notificar o outro cliente e encerrar a thread corretamente
            if mensagem.lower() == "sair":
                aviso = f"{nome_cliente} saiu do chat."
                cliente_destino.send(aviso.encode("utf-8"))
                break

            # Exibe no terminal do servidor para fins de monitoramento
            print(f"{nome_cliente}: {mensagem}")

            # Prefixa a mensagem com o nome do remetente antes de encaminhar,
            # pois o cliente destino não sabe de quem veio a mensagem
            mensagem_encaminhada = f"{nome_cliente}: {mensagem}"
            cliente_destino.send(mensagem_encaminhada.encode("utf-8"))

    except OSError as erro:
        # OSError ocorre quando um dos sockets é fechado pela outra thread
        # enquanto esta ainda tenta ler — comportamento esperado ao encerrar
        print(f"Erro na comunicação com {nome_cliente}: {erro}")

    finally:
        # Encerra ambos os lados da conversa, pois se um cliente saiu
        # não faz sentido manter o outro conectado sem par
        cliente_origem.close()
        cliente_destino.close()
        print(f"Conexão com {nome_cliente} encerrada.")


def main():
    # AF_INET = protocolo IPv4 | SOCK_STREAM = conexão TCP orientada a fluxo
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Evita o erro "Address already in use" ao reiniciar o servidor rapidamente,
    # pois o SO mantém a porta em estado TIME_WAIT por alguns segundos após o fechamento
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Associa o socket ao endereço e porta definidos
        server_socket.bind((ENDERECO_IP, PORTA))

        # Coloca o socket em modo de escuta, aceitando no máximo 2 conexões na fila
        server_socket.listen(2)

        print(f"Servidor de chat ouvindo em {ENDERECO_IP}:{PORTA}...")
        print("Aguardando dois clientes se conectarem...")

        # accept() bloqueia até um cliente conectar e retorna um novo socket
        # exclusivo para aquela conexão, além do endereço do cliente
        cliente1, endereco1 = server_socket.accept()
        print(f"Cliente 1 conectado: {endereco1}")
        cliente1.send("Você é o Cliente 1. Aguardando o Cliente 2...".encode("utf-8"))

        # Só aceita o segundo cliente após o primeiro já estar conectado,
        # garantindo que o chat só inicie com os dois presentes
        cliente2, endereco2 = server_socket.accept()
        print(f"Cliente 2 conectado: {endereco2}")

        # Notifica ambos os clientes que o chat pode começar
        cliente1.send("Cliente 2 conectado. Chat iniciado.".encode("utf-8"))
        cliente2.send("Você é o Cliente 2. Chat iniciado.".encode("utf-8"))

        # Cria duas threads simétricas: cada uma cuida de uma direção da comunicação
        # cliente1 → cliente2 e cliente2 → cliente1 rodam de forma independente e paralela
        thread1 = threading.Thread(
            target=encaminhar_mensagens,
            args=(cliente1, cliente2, "Cliente 1")
        )
        thread2 = threading.Thread(
            target=encaminhar_mensagens,
            args=(cliente2, cliente1, "Cliente 2")
        )

        thread1.start()
        thread2.start()

        # join() faz o main aguardar ambas as threads encerrarem
        # antes de prosseguir para o bloco finally
        thread1.join()
        thread2.join()

    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except OSError as erro:
        print(f"Erro no servidor: {erro}")
    finally:
        # Garante que o socket do servidor seja fechado mesmo em caso de exceção,
        # liberando a porta para uso futuro
        server_socket.close()
        print("Servidor finalizado.")

if __name__ == "__main__":
    main()