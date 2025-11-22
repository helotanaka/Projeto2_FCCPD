import time
import logging
import os
from flask import Flask, jsonify

app = Flask(__name__)

LOG_DIR = "/var/log/service"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [SERVIDOR] %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

PORT = 8080

@app.route("/")
def index():
    logger.info("Recebi requisição em /")

    response_data = {
        "status": "ok",
        "message": "oier",
        "container": "servidor",
        "timestamp": time.time(),
    }

    logger.info("Enviando resposta HTTP 200 OK.")
    return jsonify(response_data), 200


if __name__ == "__main__":
    logger.info(f"Iniciando servidor na porta {PORT}...")
    app.run(host="0.0.0.0", port=PORT)
