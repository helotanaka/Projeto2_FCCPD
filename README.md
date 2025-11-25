# Desafio 1 — Containers em Rede

## Descrição da solução

A solução é composta por dois containers que se comunicam entre si por HTTP:

- **servidor**: aplicação Flask que expõe uma rota HTTP simples e registra logs em arquivo.
- **client**: script Python que faz requisições periódicas para o servidor e também registra logs.

Os dois containers ficam na mesma rede para que possam se enxergar pelo nome do serviço.

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

## Funcionamento

1. O `docker-compose` sobe a rede `rede-desafio1` automaticamente.
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
- Toda a comunicação acontece dentro de uma **rede isolada**, com logs persistidos em volumes locais.

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
</details>

# Desafio 2 — Volumes e Persistência

## Descrição da solução

A solução demonstra **persistência de dados** usando volume com PostgreSQL.

- **banco**: container PostgreSQL que armazena dados em um volume persistente.
- **leitor**: container adicional que pode acessar os mesmos dados através do volume compartilhado.

Os dados do banco são armazenados em um volume nomeado que existe independentemente do ciclo de vida dos containers.

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

## Funcionamento

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
</details>

# Desafio 3 — Docker Compose Orquestrando Serviços

## Descrição da solução

A solução é composta por **três containers** que se comunicam entre si dentro de uma rede interna, orquestrados pelo Docker Compose:

- **database**: container que executa o banco de dados PostgreSQL.
- **cache**: container que executa o Redis para cache.
- **aplicacao**: container representando uma aplicação que se conecta ao banco de dados PostgreSQL e ao cache Redis para realizar as operações de leitura/escrita.

Os três containers ficam na mesma rede para que possam se comunicar diretamente entre si, usando os nomes dos serviços como hostnames.

- **Banco de Dados**: 
  - Imagem: PostgreSQL 15 (alpine).
  - Configurado com variáveis de ambiente para criar um banco de dados (meudb) e configurar o usuário (eu) e senha (senha).
  - Porta exposta: 5432.
  - Volume persistente: dados-postgres para armazenar os dados de forma persistente.
- **Cache**:
  - Imagem: Redis 7 (alpine).
  - Configurado com persistência de dados usando o comando --appendonly yes.
  - Porta exposta: 6379.
  - Volume persistente: dados-redis para armazenar os dados de forma persistente.
- **Aplicação**:
  - Imagem genérica (pode ser ajustada conforme necessário).
  - Conecta-se ao banco de dados PostgreSQL e ao Redis, realizando testes de comunicação.
  - Não expõe uma aplicação real, mas pode ser uma aplicação dummy para testar a conectividade entre os serviços.
  - Conecta-se ao database e ao cache através de variáveis de ambiente configuradas.

## Funcionamento

1. O comando `docker-compose` up -d sobe os três containers na rede `rede-desafio3`.
2. O container database inicia o PostgreSQL e fica escutando na porta 5432.
3. O container cache inicia o Redis e fica escutando na porta 6379.
4. O container aplicacao é iniciado e, através do comando `ping` e `nc`, verifica a comunicação com o Redis e PostgreSQL.
5. O container aplicacao também se conecta ao PostgreSQL e executa um comando `SELECT version();` para garantir que a comunicação com o banco de dados esteja funcionando.
6. Após os testes, o `comando docker-compose down -v` remove todos os containers e volumes criados.

Esse fluxo simula um cenário simples de orquestração de containers Docker, onde:
- O database oferece um serviço de banco de dados.
- O cache oferece um serviço de armazenamento em cache.
- A aplicacao consome esses serviços, garantindo que a comunicação entre os containers esteja funcionando.

<details>
   <summary><h2>Passo a passo</h2></summary>
  
  1. Ir para o diretório do desafio:
     ```bash
     cd .\Desafio3\
  
  2. Subir o container:
     ```bash
     docker-compose up -d
  
  3. Acessar o container cliente:
     ```bash
     docker exec -it cliente sh
  
  4. Testar a comunicação com o redis:
     ```bash
     ping -c 4 cache

  5. Testar a porta do postgre:
     ```bash
     pnc -zv database 5432

  6. Conectar ao postgre:
     ```bash
     psql -h database -U eu -d meudb -c "\l"

  7. Testar a versão/conexão:
     ```bash
     SELECT version();

  8. Saia do container:
     ```bash
     exit
</details>

  9. Remover os containers e volumes:
     ```bash
     docker-compose down -v
