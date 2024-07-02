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