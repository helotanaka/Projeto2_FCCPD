# Desafio 1 — Containers em Rede
# Passo a passo

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
