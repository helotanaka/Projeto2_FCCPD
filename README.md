# Desafio 1 — Containers em Rede

## Descrição da solução

A solução é composta por **dois containers Docker** que se comunicam entre si por HTTP:

- **servidor**: aplicação Flask que expõe uma rota HTTP simples.
- **client**: script Python que faz requisições periódicas para o servidor.

Os dois containers ficam na mesma **rede Docker** para que possam se enxergar pelo nome.

## Arquitetura e decisões técnicas

- **Linguagem**: Python em ambos os lados (cliente e servidor).
- **Servidor**:
  - Framework: **Flask**.
  - Rota `/` que retorna uma mensagem de texto.
  - Escuta na porta **8080** (`0.0.0.0:8080`) para ser acessível de outros containers/host.
- **Cliente**:
  - Usa a biblioteca **requests** para consumir o servidor.
  - Faz requisições em loop infinito, com **intervalo de 5 segundos**.
  - Exibe a resposta do servidor no console.
- **Docker**:
  - Cada componente (cliente e servidor) tem sua **própria imagem** e container.
  - É criada uma rede do tipo **bridge** (ex: `rede-desafio1`).
  - O servidor tem a porta **8080** exposta (`-p 8080:8080`).
  - O cliente acessa o servidor usando o hostname **`servidor`** (DNS interno do Docker).

## Funcionamento (fluxo)

1. A rede Docker é criada (ex.: `docker network create rede-desafio1`).
2. O container **servidor** é iniciado na rede e começa a escutar em `0.0.0.0:8080`.
3. O container **client** é iniciado na mesma rede.
4. Dentro do loop:
   - O cliente faz um `GET http://servidor:8080/`.
   - O servidor responde com uma mensagem fixa.
   - O cliente imprime a resposta no console.
   - Aguarda 5 segundos e repete o processo.

Esse fluxo mostra um cenário simples de **microsserviços**, onde:
- Um serviço HTTP (servidor) é exposto.
- Outro serviço (client) consome esse endpoint continuamente, tudo rodando em containers isolados.

<details>
 <summary><h2>Passo a passo</h2></summary>

1. Ir para o diretório do servidor:
   ```bash
   cd .\Desafio1\server\

2. Build da imagem do servidor:
   ```bash
   docker build -f Dockerfile -t servidor .

3. Voltar para a pasta do desafio:
   ```bash
   cd ..
   
4. Ir para o diretório do cliente:
   ```bash
   cd .\client\

5. Build da imagem do cliente:
   ```bash
   docker build -f Dockerfile -t client .

6. Criar a rede Docker:
   ```bash
    docker network create rede-desafio1

7. Subir o container do servidor
   ```bash
    docker run -d --name servidor --network rede-desafio1 -p 8080:8080 servidor

8. Subir o container do cliente:
   ```bash
    docker run -d --name client --network rede-desafio1 client

9. Ver os logs do cliente:
   ```bash
    docker logs -f client
<details>
