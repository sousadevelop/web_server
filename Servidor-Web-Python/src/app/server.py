import socket
from threading import Thread
import argparse
import sys

# Função para criar uma resposta HTTP
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

# Função para lidar com a requisição do cliente
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

# Função para parse da requisição HTTP
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

# Função para lidar com o cliente
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

# Função para iniciar o servidor
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

if __name__ == "__main__":
    start_server()
