from models.clients import Client, db
from flask import request as rq, jsonify
from os import path, getcwd, mkdir

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

    def create_client(self) -> tuple:
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

        if name and subdomain and template: # Confirma se foi passado os dados obrigatórios
            cont = 1 # Contador a somar caso a pasta ja exista
            while path.exists(self.template_dir): # Loop para caso exista mais de uma com o contador já
                self.template_dir = path.join(getcwd(), "templates", "clients", template + f'_{cont}') # Adiciona ao template_dir
                subdomain = subdomain + f"-{cont}" # Altera o subdomain também
                template = template + f'_{cont}' # Adiciona ao param do BD
                cont += 1 # Itera o contador
            mkdir(self.template_dir)

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
            with open(self.template_dir + '/index.html', "w", encoding="utf-8") as file: file.write(f""" 
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- CSS -->
    <link rel="stylesheet" href="/static/{{{{client.template}}}}/css/base.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <!-- END CSS -->

    <!-- TAG CODE -->
    {{% if analytics %}}{{{{ analytics|safe }}}}{{% else %}}<!-- NO ANALYTICS HERE-->{{% endif %}}
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

            new_client = Client( name=name, subdomain=subdomain, template = template, tel = tel ) # Cria o novo cliente e agrega os dados
            new_client.custom_domain = custom_domain if custom_domain else None # Confirma se tem o custom domain  e já agrega ao cliente criado
            db.session.add(new_client) # Adiciona a instancia a sessão
            db.session.commit() # Commita a sessão do BD
            return jsonify("Cliente criado"), 201 # Retorna a mensaem de sucesso com o codigo de created (201)
            
        return jsonify("Dados obrigatórios faltando"), 400 # Retorna BAD rq (400)

    def update_client(self) -> tuple:
        data = rq.get_json()
        id = data.get("id")
        if id:
            client = Client._search_by_id(id)
            if client:
                if data.get("name"): client.name = data.get("name")
                if data.get("custom"): client.custom_domain = data.get("custom")
                if data.get("tel"): client.tel = data.get("tel")
                if data.get("gtag"): client.gtag = data.get("gtag")
                if data.get("pixel"): client.pixel = data.get("pixel")
                if data.get("active"): client.active = data.get("active")

                return jsonify("Sucesso"), 200
            return jsonify("Cliente não encontrado"), 404
        return jsonify("ID obrigatório"), 404

    def remove_client(self) -> tuple: # Remove um cliente por ID
        """
        Remove um cliente do banco de dados com base no ID fornecido como parâmetro na query string.

        :rtype: tuple
        :return: Mensagem e status code (200 | 400 | 404)
        """
        id = rq.args.get("id") # Obtem o ID da query string
        if id: # Confirma se foi passado o ID
            client = Client.query.get(id)
            if client: # Confirma se encontrou o cliente
                db.session.delete(client) # Deleta o cliente da sessão
                db.session.commit() # Commita os dados
                return jsonify("Cliente removido"), 200 # Retorna sucesso (200)
            return jsonify("Cliente não encontrado"), 404 # Retorna NOT FOUND (404)
        return jsonify("ID Obrigatório"), 400 # Retorna BAD REQUEST (400)

