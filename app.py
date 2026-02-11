# IMPORTS UTILS
from flask import Flask, render_template, request as rq
from utils.db import db
from flask_cors import CORS
from utils.blueprints import bps
# IMPORTS SERVICES
from services.clients_service import ClientService
from services.nginx_server import NginxServer
from services.analytics import get_analytics_code
# IMPORTS ROUTES
from routes.clients_routes import clients_bp
from routes.members_routes import member_bp

"""============================================================================
===============================================================================
===============================================================================
==================== ₢ DESENVOLVIDO POR GUILHERME BREVE =======================
===============================================================================
============================================================================"""

app = Flask(__name__) # Cria o app Flask
client_service = ClientService() # Cria o service do Cliente - Utilizado no app pq é necessário para selecionar o cliente (Caso haja um)
nginx_server = NginxServer() # Cria o service do NGINX, responsavel pela estruturação de custom domain dentro do arquivo do NGINX - /etc/nginx/sites-avaible/panel.conf
CORS(app) # Flask CORS Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db" # Configuração do BANCO DE DADOS via SQLITE (Não achei necessário o uso do POSTGRES para o painel)
db.init_app(app) # Inicializa a sessão do banco de dados (Utilizando o app)

with app.app_context(): db.metadata.create_all(bind=db.engine) # Cria os bancos de dados (Caso não existam)

# Registra os blueprints necessários
for bp in bps: app.register_blueprint(bps[bp], url_prefix=bp)

# Faz a conferencia de GTAG e PIXEL CODES
@app.context_processor
def inject_analytics():
    client = client_service.resolve_client() # Resolve o cliente com base no dominio(wildcard)
    return {"analytics": get_analytics_code(client)} # Retorna o analytiics (Caso haja)

# Seta a rota principal para fazer o redirecionamento do Wildcard 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_lp(path) -> render_template:
    client = client_service.resolve_client() # Resolve o cliente com base no dominio(wildcard)
    print(client)
    if client == "panel": return render_template("panel/index.html") # COnfirma se é o painel
    if not client or not client.active: return render_template("404.html") # Confere se o cliente existe ese está ativo (Caso contrario retorna 404)
    nginx_server.config(client) # Cria os arquivos do NGINX 
    return render_template(f'clients/{client.template}/index.html') # Retorna o template correto do cliente

if __name__ == "__main__": app.run(debug=True) # Roda em modo debug (Desennvolvimento8)
