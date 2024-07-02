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