from models.clients import Client, db
from models.events import Events
from flask import request as rq, jsonify
from os import path, getcwd, mkdir
from utils.check_field import safe_route
from os import removedirs
from shutil import rmtree
from utils.extensions import ws
from datetime import datetime as dt
from utils.serializer import serialize
from utils.extensions import ws

class ClientService:
    def normalize_host(self, host: str) -> str:
        """Normaliza o host removendo www e porta(:9090) caso haja e convertendo para minusculas"""
        host = host.split(':')[0].lower()
        if host.startswith('www.'):
            host = host[4:]
        return host

    def resolve_client(self) -> Client | None:
        """ Resolve o cliente com base no dominio da requisição e retorna o Client caso encontre"""
        host = self.normalize_host(rq.host) # Normaliza o host da req.


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

    @safe_route
    def create(self, token_data) -> tuple:
        """
        Cria um novo cliente no BD de forma simples.

        :rtype: tuple
        :return: Mensagem e status code
        """

        data = rq.get_json() # Obtem os dados do JSON
        name = data.get("name") # Nome do cliente 
        subdomain = data.get("subdomain") # Subdominio
        custom_domain = data.get("custom_domain") # Dominio customizado (Opcional)
        template = data.get("template", subdomain) # Template (Com o subdominio como default)
        tel = data.get("tel") # Obtem o telefone do cliente
        self.template_dir = path.join(getcwd(), "templates", "clients", template)
        partnership_id = token_data.get("partnership_id") # Obtem o partnership_id do token para agregar ao cliente criado
        create_at = dt.now()

        if name and subdomain and template: # Confirma se foi passado os dados obrigatórios
            cont = 1 # Contador a somar caso a pasta ja exista

            while path.exists(self.template_dir): # Loop para caso exista mais de uma com o contador já
                self.template_dir = path.join(getcwd(), "templates", "clients", template +  f'_{cont}') # Adiciona ao template_dir
                new_subdomain = subdomain + f"-{cont}" # Altera o subdomain também
                new_template = template + f'_{cont}' # Adiciona ao param do BD
                cont += 1 # Itera o contador
            if cont > 1: template, subdomain = [new_template, new_subdomain] # se foi criado um contador seta o template e subdominio
            mkdir(self.template_dir) # Cria a template dir 

            static = path.join(getcwd(), 'static', template) # Obtem a rota dos assets do Static
            mkdir(static)

            css = path.join(getcwd(), 'static', template, 'css') # Obtem a rota dos assets do Static
            mkdir(css)

            js = path.join(getcwd(), 'static', template, 'js') # Obtem a rota dos assets do Static
            mkdir(js)
            
            with open(static + '/css/base.css', "w", encoding="utf-8") as css_file: css_file.write("""
            html,body { /* Added by panel */
                height: 100%;
                width: 100%;
                padding: 0;
                overflow: hidden;
            }""".strip())  # Cria o CSS Base
            open(static + '/js/main.js', "w") # Cria o JS Base
            
            # Escreve a base de criação do index.html (Modo Desenvolvimento)
            with open(self.template_dir + '/index.html', "w", encoding="utf-8") as file: 
                file.write(f""" 
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/{{{{client.template}}}}/css/base.css">
    <!-- END CSS -->

    <!-- TAG CODE -->
    {{% if analytics %}}{{{{ analytics|safe }}}}{{% else %}}<!-- NO CONFIGURED ANALYTICS -->{{% endif %}}
    <!-- END TAG CODE -->

    <title>{{{{client.name}}}}</title>
</head>

<body
    style="background-color: #222; display: flex; justify-content: center; align-items: center; color: #fff; text-align: center;">
    <div>
        <h1 style="font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;">Esta Landingpage está em
            desenvolvimento, favor entrar em contato com seu desenvolvedor!</h1>
        <h2
            style="font-style: italic; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
            This landingpage is under devlopment, please call by your developer.</h2>
    </div>

    <!-- SCRIPTS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script> AOS.init({{ duration: 2000 }}) </script>
    <script src="/static/{{{{client.template}}}}/js/main.js"></script>
    <!-- END SCRIPTS -->
</body>
</html>""".strip())
            new_client = Client( 
                name=name, subdomain=subdomain, template = template, 
                tel = tel, partnership_id = partnership_id, created_at=create_at, logo="blank.png"
            ) # Cria o novo cliente e agrega os dados
            new_client.custom_domain = custom_domain if custom_domain else None # Confirma se tem o custom domain  e já agrega ao cliente criado
            db.session.add(new_client) # Adiciona a instancia a sessão
            db.session.commit() # Commita a sessão do BD
            ws.emit("update", "new_client")
            return jsonify("Cliente criado"), 201 # Retorna a mensaem de sucesso com o codigo de created (201)
        return jsonify("Dados obrigatórios faltando"), 400 # Retorna BAD rq (400)

    @safe_route
    def read(self, token_data) -> tuple:
        partnership_id = token_data.get("partnership_id")
        clients = {
            "results": {},
            "infos": {}
        }
        if int(partnership_id) == 0: 
            clients["results"] = Client._get_all_clients()
            clients["infos"]["views"] = Events._get_count_all_views()
            clients["infos"]["clicks"] = Events._get_count_all_clicks()
        else: 
            clients["results"] = Client._search_by_partnership(partnership_id)
            clients["infos"]["views"] = Events._get_count_views_by_partnership(partnership_id)
            clients["infos"]["clicks"] = Events._get_count_clicks_by_partnership(partnership_id)
        return clients

    @safe_route
    def update(self) -> tuple:
        data = rq.get_json()
        id = data.get("id")
        type = data.get("type")
        value = data.get("value")
        msg = data.get("msg")
        
        if id:
            client = Client._search_by_id(id)
            if client:
                match type:
                    case "active": client.active = value
                    case "name": client.name = value
                    case "custom": client.custom_domain = value
                    case "tel": 
                        client.tel = value
                        client.whatsapp_msg = msg if msg else None
                    case "gtag": client.gtag = value
                    case "pixel": client.pixel = value
                db.session.commit()
                ws.emit("update", "client")
                return jsonify("Sucesso"), 200
            return jsonify("Cliente não encontrado"), 404
        return jsonify("ID obrigatório"), 404

    @safe_route
    def remove(self) -> tuple: # Remove um cliente por ID
        """
        Remove um cliente do banco de dados com base no ID fornecido como parâmetro na query string.

        :rtype: tuple
        :return: Mensagem e status code (200 | 400 | 404)
        """
        id = rq.args.get("id") # Obtem o ID da query string
        if id: # Confirma se foi passado o ID
            client = Client.query.get(id)
            if client: # Confirma se encontrou o cliente
                path_client = path.join(getcwd(), "templates", "clients", client.template)
                static_path_client = path.join(getcwd(), "static", client.template)

                # Remove as pastas e arquivos do cliente
                rmtree(path_client, ignore_errors=True)
                rmtree(static_path_client, ignore_errors=True)

                db.session.delete(client) # Deleta o cliente da sessão
                db.session.commit() # Commita os dados
                ws.emit("update", "remove_client")
                return jsonify("Cliente removido"), 200 # Retorna sucesso (200)
            return jsonify("Cliente não encontrado"), 404 # Retorna NOT FOUND (404)
        return jsonify("ID Obrigatório"), 400 # Retorna BAD REQUEST (400)