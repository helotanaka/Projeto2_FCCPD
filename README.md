# Desafio 1 — Containers em Rede

1 - ir para o diretório utlizando cd .\Desafio1\server\
2 - usar o comando docker build -f Dockerfile -t servidor .
3 - voltar para a pasta Desafio1 utilizando cd ..
4 - ir para a pasta cliente usando cd .\client\
5 - usar o comando docker build -f Dockerfile -t client .
6 - criar a rede docker: docker network create rede-desafio1
7 - rodar o docker do servidor: docker run -d  --name servidor --network rede-desafio1 -p 8080:8080 servidor
8- rodar o docker do cliente: docker run -d --name client --network rede-desafio1 client
9 - gere os logs usando o comando docker logs -f cliente