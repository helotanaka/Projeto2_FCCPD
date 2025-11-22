# Desafio 1 — Containers em Rede

## Descrição da solução

A solução é composta por **dois containers Docker** que se comunicam entre si por HTTP:

- **servidor**: aplicação Flask que expõe uma rota HTTP simples e registra logs em arquivo.
- **client**: script Python que faz requisições periódicas para o servidor e também registra logs.

Os dois containers ficam na mesma **rede Docker** para que possam se enxergar pelo nome do serviço.

- **Linguagem**: Python em ambos os lados (cliente e servidor).
- **Servidor**:
  - Framework: **Flask**.
  - Rota `/` que retorna um JSON com informações de status, mensagem, nome do container e timestamp.
  - Escuta na porta **8080** (`0.0.0.0:8080`) para ser acessível de outros containers/host.
  - Registra logs em `/var/log/service/app.log`, montado em um volume local.
- **Cliente**:
  - Usa a biblioteca **requests** para consumir o servidor.
  - Faz requisições em loop infinito, com **intervalo de 3 segundos** entre as chamadas.
  - Registra logs em `/var/log/client/app.log`, também montado em um volume local.
- **Docker:
  - Cada componente (cliente e servidor) tem sua **própria imagem** e container.
  - É criada uma rede do tipo **bridge** chamada `rede-desafio1`.
  - O servidor tem a porta **8080** exposta para o host (`8080:8080`).
  - O cliente acessa o servidor usando o hostname **`servidor`**, que é o nome do service/container na rede Docker.
  - Os logs são persistidos em diretórios locais via volumes:
    - Servidor: `./logs/servidor:/var/log/service`
    - Cliente: `./logs/client:/var/log/client`

## Funcionamento (fluxo)

1. O `docker-compose` sobe a rede Docker `rede-desafio1` automaticamente.
2. O container **servidor** é iniciado nessa rede e começa a escutar em `0.0.0.0:8080`.
3. O container **client** é iniciado na mesma rede `rede-desafio1`.
4. Dentro do loop do cliente:
   - O cliente faz um `GET http://servidor:8080/`.
   - O servidor responde com um JSON contendo informações básicas (status, mensagem, nome do container, timestamp).
   - O cliente registra no log o resultado da requisição (sucesso, erro de conexão ou timeout).
   - Aguarda 3 segundos e repete o processo.

Esse fluxo simula um cenário simples de **microsserviços**, onde:
- Um serviço HTTP (servidor) expõe um endpoint.
- Outro serviço (client) consome esse endpoint continuamente.
- Toda a comunicação acontece dentro de uma **rede Docker isolada**, com logs persistidos em volumes locais.

<details>
 <summary><h2>Passo a passo</h2></summary>

1. Ir para o diretório do servidor:
   ```bash
   cd .\Desafio1\server\

2. Subir os containers:
   ```bash
   docker compose up --build

3. Encerrar e remover containers/imagens:
   ```bash
   docker compose down --rmi local
