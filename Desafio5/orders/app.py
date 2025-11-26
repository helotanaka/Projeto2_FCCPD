from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"order_id": "A101", "user_id": 1, "product": "Laptop"},
    {"order_id": "D202", "user_id": 2, "product": "Monitor"},
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(ORDERS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)