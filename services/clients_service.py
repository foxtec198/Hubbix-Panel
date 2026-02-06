from models.clients import Client, db
from flask import request, jsonify

class ClientService:
    def normalize_host(self, host: str) -> str:
        """Normaliza o host removendo www e porta(:9090) caso haja e convertendo para minusculas"""
        host = host.split(':')[0].lower()
        if host.startswith('www.'):
            host = host[4:]
        return host

    def resolve_client(self) -> Client | None:
        """ Resolve o cliente com base no dominio da requisição e retorna o Client caso encontre"""
        host = self.normalize_host(request.host) # Normaliza o host da req.


        # domínio customizado do cliente (Caso haja)
        client = Client.query.filter_by(custom_domain=host).first()
        if client: return client # Retorna o cliente caso encontre

        # subdomínio padrão: cliente.lp.hubbix.com.br ou cliente.localhost(Modo dev apenas)
        if host.endswith('.lp.hubbix.com.br') or host.endswith(".localhost"):
            sub = host.replace('.lp.hubbix.com.br', '').replace(".localhost", "")
            if sub == "panel": return "panel"
            client = Client.query.filter_by(subdomain=sub).first()
            return client

        return None # Retorna None caso não encontre nenhum cliente

    def create_client(self) -> tuple:
        """
        Cria um novo cliente no BD de forma simples.

        :rtype: tuple
        :return: Mensagem e status code
        """

        data = request.get_json() # Obtem os dados do JSON
        name = data.get("name") # Nome do cliente 
        subdomain = data.get("subdomain") # Subdominio
        custom_domain = data.get("custom_domain") # Dominio customizado (Opcional)
        template = data.get("template", subdomain) # Template (Com o subdominio como default)

        if name and subdomain and template: # Confirma se foi passado os dados obrigatórios
            new_client = Client( name=name, subdomain=subdomain, template = template ) # Cria o novo cliente e agrega os dados
            new_client.custom_domain = custom_domain if custom_domain else None # Confirma se tem o custom domain  e já agrega ao cliente criado
            db.session.add(new_client) # Adiciona a instancia a sessão
            db.session.commit() # Commita a sessão do BD
            return jsonify("Cliente criado"), 201 # Retorna a mensaem de sucesso com o codigo de created (201)
        return jsonify("Dados obrigatórios faltando"), 400 # Retorna BAD REQUEST (400)

    def remove_client(self) -> tuple: # Remove um cliente por ID
        """
        Remove um cliente do banco de dados com base no ID fornecido como parâmetro na query string.

        :rtype: tuple
        :return: Mensagem e status code (200 | 400 | 404)
        """
        id = request.args.get("id") # Obtem o ID da query string
        if id: # Confirma se foi passado o ID
            client = Client.query.get(id)
            if client: # Confirma se encontrou o cliente
                db.session.delete(client) # Deleta o cliente da sessão
                db.session.commit() # Commita os dados
                return jsonify("Cliente removido"), 200 # Retorna sucesso (200)
            return jsonify("Cliente não encontrado"), 404 # Retorna NOT FOUND (404)
        return jsonify("ID Obrigatório"), 400 # Retorna BAD REQUEST (400)

