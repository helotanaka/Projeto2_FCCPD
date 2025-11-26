from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/usuarios-detalhados', methods=['GET'])
def get_usuarios_detalhados():
    try:
        resposta = requests.get('http://servico1:5000/usuarios')
        usuarios = resposta.json()
        
        resultado = []
        for user in usuarios:

            resultado.append({
                "info": f"Usuario {user['nome']} tem a profissao {user['profissão']}",
                "id": user['id']
            })
        
        return jsonify(resultado)
    except:
        return jsonify({"erro": "Não conseguiu conectar no service_a"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)