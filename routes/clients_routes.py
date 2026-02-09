from flask import Blueprint, request, render_template
from services.clients_service import ClientService

service_client = ClientService()
clients_bp = Blueprint('Clientes', __name__)

@clients_bp.route("", methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS", "HEAD"])
def main():
    match request.method:
        case "POST": return service_client.create_client()
        case "DELETE": return service_client.remove_client()
    return render_template("404.html")