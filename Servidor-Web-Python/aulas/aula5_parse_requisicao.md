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