from flask import request as rq, jsonify
from models.events import Events, db
from utils.check_field import safe_route
from datetime import datetime as dt, timedelta
from hashlib import sha256

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
        client_id = client["id"]
        user_agent = rq.headers.get("User-Agent", "")
        ip = rq.headers.get("CF-Connecting-IP", rq.headers.get("X-Forwarded-For", rq.remote_addr))
        fingerprint = sha256(f"{ip}:{user_agent}".encode()).hexdigest()

        if type == "VIEW":
            limit_date = dt.now() - timedelta(hours=8)

            event_exists = Events.query.filter(
                Events.client_id == client_id,
                Events.fingerprint == fingerprint,
                Events.type == "VIEW",
                Events.date >= limit_date
            ).first()

            if not event_exists:
                new_event = Events(client_id=client_id, ip=ip, date=dt.now(), fingerprint=fingerprint, type=type)
                db.session.add(new_event)
                db.session.commit()
                return jsonify(new_event.to_dict())
        else:
            new_event = Events(client_id=client_id, ip=ip, date=dt.now(), fingerprint=fingerprint, type=type)
            db.session.add(new_event)
            db.session.commit()
            return jsonify(new_event.to_dict())