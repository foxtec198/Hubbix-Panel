from flask import Blueprint, request, render_template
from services.events_service import EventService
from services.gh import GitHub

event_client = EventService()
events_bp = Blueprint('Eventos', __name__)

@events_bp.route("", methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS", "HEAD"])
def main():
    match request.method:
        case "GET": return event_client.read()
        case "POST": 
            data = request.get_json()
            return event_client.create(data.get("client"), data.get("type"))
    return render_template("404.html")