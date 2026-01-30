from models.client import Client, db
from flask import request, jsonify

class ClientService:
    def normalize_host(self, host: str) -> str:
        host = host.split(':')[0].lower()
        if host.startswith('www.'):
            host = host[4:]
        return host

    def resolve_client(self) -> Client | None:
        host = self.normalize_host(request.host)

        # domínio customizado
        client = Client.query.filter_by(custom_domain=host).first()
        if client: return client

        # subdomínio padrão: cliente.lp.hubbix.com.br
        if host.endswith('.lp.hubbix.com.br') or host.endswith(".localhost"):
            sub = host.replace('.lp.hubbix.com.br', '').replace(".localhost", "")
            return Client.query.filter_by(subdomain=sub).first()

        return None

    def create_client(self) -> tuple:
        data = request.get_json()
        name = data.get("name")
        subdomain = data.get("subdomain")
        custom_domain = data.get("custom_domain")
        template = data.get("template", subdomain)

        if name and subdomain and template:
            new_client = Client( name=name, subdomain=subdomain, template = template )
            new_client.custom_domain = custom_domain if custom_domain else None
            db.session.add(new_client)
            db.session.commit()
            return jsonify("Cliente criado"), 201
        return jsonify("Dados obrigatórios faltando"), 400

    def remove_client(self) -> tuple:
        id = request.args.get("id")
        if id:
            client = Client.query.get(id)
            if client:
                db.session.delete(client)
                db.session.commit()
                return jsonify("Cliente removido"), 200
            return jsonify("Cliente não encontrado"), 404
        return jsonify("ID Obrigatório"), 400

