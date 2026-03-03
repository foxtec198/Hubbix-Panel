from flask import Blueprint, request, render_template
from services.login_service import LoginService

login_service = LoginService()
login_bp = Blueprint('Login', __name__)

@login_bp.route("", methods=["GET", "POST", "DELETE", "PATCH"])
def main():
    match request.method:
        case "POST": return login_service.login()