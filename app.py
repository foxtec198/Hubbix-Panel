# IMPORTS
from flask import Flask, render_template, abort, request as rq
from models.client import db
from services.clients_service import ClientService
from routes.clients_routes import clients_routes
from flask_cors import CORS

"""============================================================================
===============================================================================
===============================================================================
==================== ₢ DESENVOLVIDO POR GUILHERME BREVE =======================
===============================================================================
============================================================================"""

app = Flask(__name__) # Cria o app Flask
service_client = ClientService()
CORS(app) # Flask CORS Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.db" # Configuração do BANCO DE DADOS via SQLITE (Não achei necessário o uso do POSTGRES para o painel)
db.init_app(app) # Inicializa a sessão do banco de dados (Utilizando o app)

# Cria os bancos de dados (Caso não existam)
with app.app_context(): db.metadata.create_all(bind=db.engine)

# Registra os blueprints necessários
app.register_blueprint(clients_routes, url_prefix="/clientes") 

# Seta a rota principal para fazer o redirecionamento do Wildcard 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_lp(path) -> render_template:
    client = service_client.resolve_client() # Resolve o cliente com base no dominio(wildcard)

    if not client or not client.active: return render_template("404.html") # Confere se o cliente existe ese está ativo (Caso contrario retorna 404)
    return render_template(f'clients/{client.template}/index.html') # Retorna o template correto do cliente

if __name__ == "__main__": app.run(debug=True) # Roda em modo debug (Desennvolvimento8)
