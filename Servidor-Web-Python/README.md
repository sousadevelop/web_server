# Servidor Web em Python

Bem-vindo ao repositório **Servidor Web em Python**! Este projeto tem como objetivo ensinar como construir um servidor web simples em Python, abordando conceitos fundamentais de redes e desenvolvimento web.

## Estrutura do Projeto


### Funcionalidades

- **Requisições GET e POST:** Suporte para métodos HTTP GET e POST.
- **Serviço de Arquivos:** Capacidade de servir arquivos de um diretório especificado.
- **Respostas Personalizadas:** Respostas com diferentes códigos de status HTTP.

### Requisitos

- Python 3.x

### Como Usar

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/Servidor-Web-Python.git
    cd Servidor-Web-Python
    ```

2. **Navegue até o diretório `src`:**
    ```bash
    cd src
    ```

3. **Execute o servidor:**
    ```bash
    python server.py --directory ./files
    ```

4. **Acesse o servidor:**
    Abra o navegador e vá para `http://localhost:4221`.

## Estrutura das Aulas

As aulas estão organizadas de maneira sequencial para guiar você desde a introdução até a implementação completa do servidor:

1. **[Introdução](aulas/aula1_introducao.md):** Visão geral do projeto.
2. **[Importação de Bibliotecas](aulas/aula2_importacao_bibliotecas.md):** Bibliotecas necessárias para o projeto.
3. **[Resposta HTTP](aulas/aula3_resposta_http.md):** Como criar uma resposta HTTP.
4. **[Requisições do Cliente](aulas/aula4_requisicoes_cliente.md):** Lidando com requisições do cliente.
5. **[Parse da Requisição](aulas/aula5_parse_requisicao.md):** Como analisar a requisição HTTP.
6. **[Lidando com o Cliente](aulas/aula6_lidando_cliente.md):** Conectando-se e respondendo ao cliente.
7. **[Iniciando o Servidor](aulas/aula7_iniciando_servidor.md):** Configuração e inicialização do servidor.
8. **[Executando o Servidor](aulas/aula8_executando_servidor.md):** Ponto de entrada do script.

## Como Contribuir

1. **Fork o projeto**
2. **Crie uma nova branch:**
    ```bash
    git checkout -b minha-nova-funcionalidade
    ```
3. **Faça suas alterações e commit:**
    ```bash
    git commit -m 'Adiciona nova funcionalidade'
    ```
4. **Envie para o repositório original:**
    ```bash
    git push origin minha-nova-funcionalidade
    ```
5. **Crie um pull request**

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Esperamos que este projeto ajude você a entender melhor como construir um servidor web básico em Python. Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para abrir uma issue ou contribuir diretamente no repositório.
