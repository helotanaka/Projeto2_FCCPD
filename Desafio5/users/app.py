from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Antonio", "email": "antonio@example.com"},
    {"id": 2, "name": "Davi", "email": "davi@example.com"},
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(USERS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)