import time
import requests
import logging
import os

LOG_DIR = "/var/log/client"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [CLIENTE] %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

SERVER_URL = "http://servidor:8080"
WAIT_TIME = 3 

def make_request():
    try:
        logger.info(f"Tentando acessar {SERVER_URL}...")
        response = requests.get(SERVER_URL, timeout=3)

        if response.status_code == 200:
            logger.info(f"✅ Resposta 200 OK: {response.text}")
        else:
            logger.warning(f"⚠️ Resposta com status {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        logger.error("❌ ERRO! Não foi possível conectar ao servidor. O servidor está pronto?")
    except requests.exceptions.Timeout:
        logger.error("❌ ERRO! Tempo limite de conexão esgotado.")
    except Exception as e:
        logger.error(f"❌ ERRO inesperado: {e}")

def main():
    logger.info("Iniciando cliente de requisições periódicas...")
    while True:
        make_request()
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
