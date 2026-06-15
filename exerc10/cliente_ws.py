# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import asyncio # Gerencia as tarefas simultâneas.
import websockets # Faz a conexão com o servidor.
import sys # Manipula I/O no terminal

ENDERECO_IP = input("Informe o endereço IP do cliente: ")
PORTA = int(input("Informe uma porta: "))

async def receber_mensagens(websocket, nome):
    try:
        # Loop que pausa e aguarda por novas mensagens
        async for mensagem in websocket:
            # \r volta ao início da linha
            # \033[K apaga o que estava escrito na linha
            # Imprime a mensagem recebida, quebra a linha e coloca o username no início da linha
            sys.stdout.write(f"\r\033[K{mensagem}\n{nome}: ")
            sys.stdout.flush()
    except asyncio.CancelledError:
        # Cancelamento esperado quando o cliente estiver encerrando.
        pass
    except websockets.exceptions.ConnectionClosed:
        print("\r\033[KA Conexão com o servidor foi encerrada!.")

async def enviar_mensagens(websocket, nome):
    # Usa o loop atual para observar o stdin sem travar o chat.
    loop = asyncio.get_running_loop()
    # Recebe as linhas digitadas no terminal.
    leitor = asyncio.StreamReader()
    # Faz a ponte entre o stdin e o leitor assíncrono.
    protocolo = asyncio.StreamReaderProtocol(leitor)
    await loop.connect_read_pipe(lambda: protocolo, sys.stdin)

    while True:
        # Mostra o prompt antes de esperar a próxima linha.
        sys.stdout.write(f"{nome}: ")
        sys.stdout.flush()

        # Lê uma linha sem bloquear o recebimento das mensagens.
        mensagem = (await leitor.readline()).decode().rstrip("\n")

        # Condicional para tratamento para mensagens vazias
        if mensagem.strip():
            try:
                await websocket.send(mensagem)
            except websockets.exceptions.ConnectionClosed:
                print("A conexão com o servidor foi encerrada. Não é possível enviar.")
                break
        else:
            # \033[F sobe o cursor para a linha anterior (onde o usuário deu enter vazio)
            # \033[K apaga a linha
            sys.stdout.write("\033[F\033[K")
            sys.stdout.write("Erro: Mensagem vazia não permitida.\n")
            sys.stdout.flush()

async def start_cliente():
    nome = input("Digite seu nome para entrar no chat: ")
    # Estabelece conexão com o servidor
    async with websockets.connect(f"ws://{ENDERECO_IP}:{PORTA}") as websocket:
        await websocket.send(nome)

        # Recebe o nome definitivo do servidor
        nome_confirmado = await websocket.recv()
        
        if nome != nome_confirmado:
            print(f"Aviso: Já tem alguém com o username '{nome}'. Seu username será '{nome_confirmado}'.")
            print("Conectado ao chat! Digite sua mensagem!")
        else:
            print("Conectado ao chat! Digite sua mensagem!")

        # Executa simultâneamente as tarefas de envio e recebimento de mensagens
        await asyncio.gather(
            receber_mensagens(websocket, nome_confirmado),
            enviar_mensagens(websocket, nome_confirmado)
        )

# Inicia o cliente
try:
    asyncio.run(start_cliente())
except KeyboardInterrupt:
    print("Cliente finalizado.")