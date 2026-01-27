from flask import Flask, render_template, abort, request as rq
from models.client import db
from services.clients_service import ClientService
from routes.clients_routes import clients_routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.db"
db.init_app(app)

with app.app_context(): db.metadata.create_all(bind=db.engine)
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_lp(path):
    service_client = ClientService()
    client = service_client.resolve_client()

    if not client or not client.active:
        return render_template("404.html")

    return render_template(
        f'clients/{client.template}/index.html',
        client=client
    )    

app.register_blueprint(clients_routes, url_prefix="/clientes")

if __name__ == "__main__": 
    app.run(debug=True)
