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
- **Docker**:
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
  <details>
# Desafio 2 — Volumes e Persistência

## Descrição da solução

A solução demonstra **persistência de dados** usando **Docker Volumes** com PostgreSQL.

- **banco**: container PostgreSQL que armazena dados em um volume persistente.
- **leitor**: container adicional que pode acessar os mesmos dados através do volume compartilhado.

Os dados do banco são armazenados em um **volume nomeado** (`volume-postgres`) que existe **independentemente** do ciclo de vida dos containers.

- **Banco de dados**: PostgreSQL
- **Servidor (banco)**:
  - Imagem: **postgres:15-alpine**.
  - Expõe a porta **5050** para acesso externo.
  - Credenciais configuradas via variáveis de ambiente:
    - Usuário: `eu`
    - Senha: `senha`
    - Database: `meudb`
  - Dados persistidos em: `volume-postgres:/var/lib/postgresql/data`
- **Leitor**:
  - Mesma imagem PostgreSQL, mas usado apenas para **leitura/verificação**.
  - Acessa o **mesmo volume** que o container banco.
- **Docker**:
  - Volume nomeado **`volume-postgres`** gerenciado pelo Docker.
  - Rede do tipo **bridge** chamada `rede-desafio2` para comunicação entre containers.

## Funcionamento (fluxo)

1. O `docker-compose` cria o volume `volume-postgres` e a rede `rede-desafio2` automaticamente.
2. O container **banco** é iniciado e o PostgreSQL armazena todos os dados no volume.
3. Dados são inseridos no banco através de comandos SQL:
   - Criação de tabelas (ex: `produtos`)
   - Inserção de registros
4. O container **banco** é **parado e removido** completamente.
5. Um **novo container banco** é criado usando o **mesmo volume**.
6. Ao consultar o banco novamente, os dados **continuam lá**, provando a persistência.

 <details>
   <summary><h2>Passo a passo</h2></summary>
  
  1. Ir para o diretório do desafio:
     ```bash
     cd .\Desafio2\
  
  2. Subir o container:
     ```bash
     docker-compose up -d banco
  
  3. Conectar no banco:
     ```bash
     docker exec -it postgres-desafio2 psql -U eu -d meudb

 4. Inserir tabelas e produtos:
     ```bash
      CREATE TABLE produtos (id SERIAL PRIMARY KEY, nome VARCHAR(100), preco DECIMAL(10,2));
     ```
     ```bash
      INSERT INTO produtos (nome, preco) VALUES ('Notebook', 3500.00), ('Mouse', 50.00), ('Teclado', 150.00);
     ```
     ```bash
     SELECT * FROM produtos;
     ```
     <img width="1253" height="313" alt="image" src="https://github.com/user-attachments/assets/11a0b6ba-fb40-4fa3-a230-3c5fc8951ac1" />

5. Fechar o banco com Ctrl + D

6. Remover o container:
  ```bash
  docker-compose down
  ```
7. Confirmar a remoção:
``` bash
docker ps -a
```
<img width="1546" height="135" alt="image" src="https://github.com/user-attachments/assets/4ddb8118-a839-4274-9bec-126134922ef8" />

 8. Subir novamente o container:
     ```bash
     docker-compose up -d banco
     
9. Ver se os dados persistem:
     ```bash
     docker exec -it postgres-desafio2 psql -U eu -d meudb -c "SELECT * FROM produtos;"

<img width="1573" height="298" alt="image" src="https://github.com/user-attachments/assets/1e872ef3-710a-4b17-bb59-46573c5cf380" />

10. Remover os itens criados:
     ```bash
     docker-compose down -v

  <details>
