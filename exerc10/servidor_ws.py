# Discentes: Juan Pablo Ferreira Costa, Nadson Nascimento Santos e Vitor Mozer Vieira Sales

import asyncio
import websockets

try:
    ENDERECO_IP = input("Informe o endereço IP do servidor: ")
    PORTA = int(input("Informe uma porta(0 para o SO escolher automaticamente): "))
except KeyboardInterrupt:
    print("\nServidor finalizado.")
    raise SystemExit
conexoes_ativas = {} # Armazena os sockets conectados e seus respectivos nomes
contadores_nomes = {} # Gerencia a numeração para nomes duplicados

async def registrar_usuario(websocket):
    nome_usuario = await websocket.recv()
    # Verifica se alguém online está usando o username informado
    if nome_usuario in conexoes_ativas.values():
        nome_base = nome_usuario 
        # Lógica para definição do sufixo do username
        if nome_base not in contadores_nomes:
            contadores_nomes[nome_base] = 2
        else:
            contadores_nomes[nome_base] += 1
            
        nome_usuario = f"{nome_base}_{contadores_nomes[nome_base]}"
        
        # Loop de segurança para caso do cliente informar o username com sufixo manualmente
        while nome_usuario in conexoes_ativas.values():
            contadores_nomes[nome_base] += 1
            nome_usuario = f"{nome_base}_{contadores_nomes[nome_base]}"

    conexoes_ativas[websocket] = nome_usuario
    print(f"{nome_usuario} está conectado. Total de usuários conectados: {len(conexoes_ativas)}")
    # Envia uma mensagem particular para o cliente informando sobre o seu username
    await websocket.send(nome_usuario)
    return nome_usuario

async def gerenciar_conexoes(websocket):
    nome_usuario = None
    try:
        nome_usuario = await registrar_usuario(websocket)

        async for mensagem in websocket:
            # Validação do servidor para mensagens vazias por segurança (cliente já trata isso)
            if not mensagem.strip():
                continue

            print(f"{nome_usuario}: {mensagem}")

            # Envia a mensagem para todos os clientes, exceto para quem a enviou.
            for cliente in conexoes_ativas:
                if cliente != websocket:
                    await cliente.send(f"{nome_usuario}: {mensagem}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Aviso: A conexão com o cliente foi interrompida. Detalhes: {e}")
    except Exception as e:
        # Captura qualquer outro erro inesperado que não seja de conexão
        print(f"Erro inesperado no servidor: {e}")
    finally:
        # Remove o cliente das conexões ativas caso perca a conexão
        if websocket in conexoes_ativas:
            nome_desconectado = conexoes_ativas[websocket]
            del conexoes_ativas[websocket]
            print(f"[{nome_desconectado}] perdeu a conexão! Total de usuários conectados: {len(conexoes_ativas)}")

async def start_servidor():
    async with websockets.serve(gerenciar_conexoes, ENDERECO_IP, PORTA) as servidor:
        if PORTA == 0:
            porta_real = servidor.sockets[0].getsockname()[1]
        else:
            porta_real = PORTA
        print(f"Servidor ouvindo em {ENDERECO_IP}:{porta_real}...")
        await asyncio.Future()

# Inicia o servidor
try:
    asyncio.run(start_servidor())
except KeyboardInterrupt:
    print("Servidor finalizado.")