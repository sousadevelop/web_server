# Curso de Construção de Servidor Web em Python

## Aula 1: Introdução

### Objetivo
Construir um servidor web simples em Python, que responde a diferentes tipos de requisições HTTP.

### Estrutura do Código
O código é dividido em várias funções que lidam com diferentes aspectos da comunicação HTTP e a estrutura do servidor. Vamos explorar cada parte detalhadamente.

-----------------------------------------------------------------------------------

## Aula 2: Importação de Bibliotecas

```python
import socket
from threading import Thread
import argparse
import sys
```

### Explicação
 - **socket:** Biblioteca padrão do Python usada para criar sockets, permitindo comunicação de rede.
 - **threading:** Biblioteca que permite a criação de threads, permitindo que nosso servidor lide com múltiplas conexões simultaneamente.
 - **argparse:** Biblioteca que facilita a criação de interfaces de linha de comando, permitindo que nosso servidor aceite argumentos ao ser executado.
 - **sys:** Biblioteca que fornece acesso a algumas variáveis e funções do interpretador Python.

------------------------------------------------

## Aula 3: Criando uma Resposta HTTP

```python
def reply(code, body="", headers={}):
    b_reply = b""
    if code == 200:
        b_reply += b"HTTP/1.1 200 OK\r\n"
    elif code == 201:
        b_reply += b"HTTP/1.1 201 Created\r\n"
    elif code == 404:
        b_reply += b"HTTP/1.1 404 Not Found\r\n"
    elif code == 500:
        b_reply += b"HTTP/1.1 500 Internal Server Error\r\n"
    elif code == 405:
        b_reply += b"HTTP/1.1 405 Method Not Allowed\r\n"
    
    if "Content-Type" not in headers:
        headers["Content-Type"] = "text/plain"
    if body:
        headers["Content-Length"] = str(len(body))
    
    for key, val in headers.items():
        b_reply += bytes(f"{key}: {val}\r\n", "utf-8")
    b_reply += b"\r\n" + bytes(body, "utf-8")
    return b_reply
```

### Explicação
 - Objetivo: Criar uma resposta HTTP formatada.
 - Parâmetros:
    - code: Código de status HTTP (e.g., 200, 404).
    - body: Corpo da resposta HTTP.
    - headers: Dicionário contendo cabeçalhos HTTP.
 - Implementação:
    - A função monta a resposta começando pela linha de status.
Adiciona cabeçalhos, incluindo Content-Type e Content-Length.
Junta todos os componentes em um único byte string (b_reply).

------------------------------------------------

## Aula 4: Lidando com Requisições do Cliente

```python
def handle_request(req):
    if req["method"] == "GET":
        if req["path"] == "/":
            return reply(200, "Welcome to my page!")
        elif req["path"].startswith("/echo/"):
            return reply(200, req["path"][6:])
        elif req["path"] == "/user-agent":
            ua = req["headers"].get("User-Agent", "Unknown")
            return reply(200, ua)
        elif req["path"].startswith("/files/"):
            filename = req["path"][7:]
            try:
                with open(f"{base_directory}/{filename}", "r") as f:
                    body = f.read()
                headers = {"Content-Type": "application/octet-stream"}
                return reply(200, body, headers)
            except Exception:
                return reply(404, "Page not found.")
    elif req["method"] == "POST":
        if req["path"].startswith("/files/"):
            filename = req["path"][7:]
            try:
                with open(f"{base_directory}/{filename}", "wb") as f:
                    f.write(req["body"].encode())
                return reply(201)
            except Exception:
                return reply(500, "Internal Server Error")
    return reply(404, "Page not found.")
```

### Explicação

 - Objetivo: Processar a requisição HTTP e determinar a resposta apropriada.
 - Implementação:
    - GET Requests:
      - /: Responde com uma mensagem de boas-vindas.
      - /echo/: Responde com a parte da URL após /echo/.
      - /user-agent: Responde com o valor do cabeçalho User-Agent.
      - /files/: Lê e retorna o conteúdo de um arquivo especificado.
    - POST Requests:
      - /files/: Cria ou sobrescreve um arquivo com o corpo da requisição.
      - Fallback: Responde com 404 Not Found para requisições não tratadas.

-------------------------------------------------------------

## Aula 5: Parse da Requisição HTTP

```python
def parse_request(data):
    output = {"method": "", "path": "", "headers": {}, "body": ""}
    lines = data.decode("utf-8").split("\r\n")
    if len(lines) < 3:
        return None
    req_line = lines[0].split(" ")
    if not req_line[0] or req_line[0] not in ["GET", "POST", "PUT", "HEAD"]:
        return None
    if not req_line[1] or req_line[1][0] != "/":
        return None
    output["method"] = req_line[0]
    output["path"] = req_line[1]
    headers_section = lines[1:]
    for i, line in enumerate(headers_section):
        if line == "":
            break
        header, value = line.split(":", 1)
        output["headers"][header.strip()] = value.strip()
    output["body"] = "\r\n".join(headers_section[i+1:])
    return output
```

### Explicação
  - Objetivo: Analisar os dados da requisição HTTP e extrair método, caminho, cabeçalhos e corpo.
  - Implementação:
      - Divide os dados da requisição em linhas.
      - Separa a linha de requisição (método e caminho).
      - Lê e armazena cabeçalhos.
      - Lê o corpo da requisição.

------------------------------------------------------------------

## Aula 6: Lidando com o Cliente

```python
def handle_client(conn):
    try:
        data = conn.recv(1024)
        if not data:
            return
        parsed_req = parse_request(data)
        if not parsed_req:
            conn.sendall(reply(500))
            conn.close()
            return
        response = handle_request(parsed_req)
        conn.sendall(response)
    except Exception as e:
        print("handle_client error:", e)
        conn.sendall(reply(500))
    finally:
        conn.close()
```

### Explicação

  - Objetivo: Lidar com a conexão do cliente, processar a requisição e enviar a resposta.
  - Implementação:
    - Recebe os dados do cliente.
    - Analisa a requisição.
    - Gera a resposta apropriada.
    - Envia a resposta e fecha a conexão.
   
-----------------------------------------------------------------------

## Aula 7: Iniciando o Servidor

```python
def start_server():
    parser = argparse.ArgumentParser(description="Servidor HTTP simples que serve arquivos de um diretório especificado.")
    parser.add_argument('--directory', type=str, default=".", help='Diretório base para servir arquivos. (default: diretório atual)')
    args = parser.parse_args()

    global base_directory
    base_directory = args.directory

    print("Iniciando o servidor na porta 4221...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 4221))
    server_socket.listen(1)

    try:
        while True:
            print("Esperando por conexão...")
            conn, addr = server_socket.accept()
            print(f"Conexão estabelecida com {addr}")
            t = Thread(target=handle_client, args=(conn,))
            t.start()
    except KeyboardInterrupt:
        print("\nServidor desligando...")
    finally:
        server_socket.close()
        print("Servidor desligado.")
```

### Explicação

  - Objetivo: Configurar e iniciar o servidor para aceitar conexões.
  - Implementação:
    - Usa argparse para aceitar um diretório base como argumento.
    - Cria e configura um socket do servidor.
    - Coloca o servidor em modo de escuta (listen).
    - Aceita conexões e cria uma nova thread para cada conexão.

------------------------------------------------

## Aula 8: Executando o Servidor

```python
if __name__ == "__main__":
    start_server()
```

### Explicação

  - Objetivo: Ponto de entrada do script, inicia o servidor.
  - Implementação:
    - Chama a função start_server para iniciar o servidor quando o script é executado.

-------------------------------------

## Conclusão

Neste curso, construímos um servidor web básico em Python, que pode lidar com requisições GET e POST, responder com diferentes códigos de status e servir arquivos de um diretório especificado. Este servidor pode ser uma base sólida para aprender conceitos mais avançados de redes e desenvolvimento web.
