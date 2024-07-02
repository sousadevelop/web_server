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