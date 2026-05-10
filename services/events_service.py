from flask import request as rq, jsonify
from models.events import Events, db
from utils.check_field import safe_route
from datetime import datetime as dt

class EventService:
    @safe_route
    def read(self, token_data):
        partnership_id = token_data["partnership_id"] 
        client_id = rq.args.get("id")
        eventos = {}
        if partnership_id == 0: eventos = Events.query.all()
        if partnership_id > 0: eventos = Events.query.filter_by(partnership_id=partnership_id).all()
        if client_id: eventos = Events.query.filter_by(client_id=client_id).all()

        return jsonify([evento.to_dict() for evento in eventos])

    def create(self, client, type):
        user_agent = rq.headers.get("User-Agent", "")
        ip = rq.headers.get(
            "CF-Connecting-IP",
            rq.headers.get(
                "X-Forwarded-For",
                rq.remote_addr
            )
        )
        client_id = client["id"]
        partnership_id = client["partnership_id"]
        new_event = Events(
            client_id=client_id, partnership_id=partnership_id,
            ip= ip, date=dt.now(), user_agent=user_agent, type=type
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict())