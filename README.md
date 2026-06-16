# Sockets TCP e UDP no Python

Esse é um trabalho da disciplina de Redes de Computadores II que visa explorar o uso de sockets TCP e UDP para comunicação entre clientes e servidores. O projeto foca na arquitetura Cliente-Servidor, utilizando tanto Sockets puros (TCP e UDP) quanto WebSockets assíncronos.

## Integrantes
- Juan Pablo Ferreira Costa
- Nadson Nascimento Santos
- Vitor Mozer Vieira Sales

## Como Executar o Projeto

O repositório está dividido entre as questões que utilizam bibliotecas nativas do Python (Questões 1 a 4) e a Questão 10, que exige uma configuração específica (Criação e ativação de ambiente virtual e instalação de biblioteca). Siga as instruções abaixo de acordo com a questão que deseja testar.

### Questões de 1 a 4 (Sockets TCP/UDP)

As questões baseadas em Sockets TCP e UDP utilizam apenas bibliotecas nativas do Python. Portanto, **não é necessário** utilizar ambiente virtual (`.venv`) ou instalar bibliotecas externas.

**Passo 1: Executar o servidor**  
- Abra um terminal, navegue até a pasta da questão correspondente (se houver) e inicie o arquivo do servidor. Exemplo:
```bash
python3 server.py
```

**Passo 2: Executar o Cliente**  
- Abra um **novo terminal** e inicie o arquivo do cliente correspondente:
```bash
python3 cliente.py
```
*(Quando for o caso, para testar múltiplas conexões simultâneas, basta abrir novos terminais e executar o comando do cliente novamente).*

---

### Questão 10 (Chat com WebSockets)

Esta aplicação utiliza a biblioteca externa `websockets`. Para isolar as dependências e evitar conflitos no sistema, é necessário configurar um ambiente virtual (`.venv`).

Siga os passos abaixo na pasta raiz do projeto pelo terminal Linux:

**Passo 1: Criar o ambiente virtual**
```bash
python3 -m venv .venv
```

**Passo 2: Ativar o ambiente virtual**
```bash
source .venv/bin/activate
```
*(O prefixo `(.venv)` no início da linha do terminal indica que o ambiente virtual está ativo)*

**Passo 3: Instalar as dependências**  
- Com o ambiente ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

**Passo 4: Executar o Servidor**  
- Ainda com o ambiente ativado, inicie o servidor:
```bash
python3 exerc10/servidor_ws.py
```

**Passo 5: Executar os Clientes**  
- Abra novos terminais para simular múltiplos usuários.  

*(OBS: É necessário ativar o ambiente virtual em cada novo terminal antes de executar o arquivo cliente_ws.py)*
```bash
source .venv/bin/activate
python3 exerc10/cliente_ws.py
```