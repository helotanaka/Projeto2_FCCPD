from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERS_SERVICE_URL = "http://users:5001"
ORDERS_SERVICE_URL = "http://orders:5002"

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        response = requests.get(f"{USERS_SERVICE_URL}/users")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erro ao comunicar com o serviço de usuários", "details": str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        response = requests.get(f"{ORDERS_SERVICE_URL}/orders")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erro ao comunicar com o serviço de pedidos", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)