from flask import request as rq, Blueprint
from services.nginx_server import NginxServer

custom_domain_bp = Blueprint("Dominios Customizados", __name__)
server_service = NginxServer()

@custom_domain_bp.route("", methods=["GET", "POST", "UPDATE", "DELETE"])
def main():
    match rq.method:
        case "POST": return server_service.config()