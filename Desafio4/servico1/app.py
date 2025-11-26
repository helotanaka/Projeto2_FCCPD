from flask import Flask, jsonify

app = Flask(__name__)

usuarios = [
    {"id": 1, "nome": "Rafael", "profissão": "desenvolvedor"},
    {"id": 2, "nome": "Jorge", "profissão": "professor"},
    {"id": 3, "nome": "Larissa", "profissão": "pequisador"}
]

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)