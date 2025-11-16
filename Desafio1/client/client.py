import time
import requests

SERVER_URL = "http://servidor:8080"

while True:
    print("Fazendo requisição para o servidor...")
    try:
        response = requests.get(SERVER_URL)
        print(response.text)
    except Exception as e:
        print(f"Erro: {e}")
    time.sleep(5)
