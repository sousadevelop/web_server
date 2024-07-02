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