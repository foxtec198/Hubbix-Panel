from models.clients import Client
from os import path, getcwd
from subprocess import call

class NginxServer():
    model_filename = path.join(getcwd(), "models", "nginx_model.conf")
    # location = path.join("//etc", "nginx", "sites-available", "panel.conf")
    location = "/etc/nginx/sites-available/panel.conf"

    def config(self, client:Client) -> None: # Configura o arquivo do nginx
        if client and client.custom_domain and path.exists(self.location): # Confirma se existe a configuração do PAINEL no NGINX e se o cliente tem um custom domain
            with open(self.location, "r") as old_file: file = old_file.read() # Le os dados do arquivo antes de atualizar (Old)
            if not file.__contains__(client.custom_domain): # Confirma se o domnio ja existe no arquivo
                with open(self.model_filename, "r", encoding="utf-8") as file: default = file.read() # Le os dados do MODELO do Nginx (Com HTTPS)
                new_txt = default.replace("[CLIENT_ID]", client.name.upper() # Altera o nome de identificação
                ).replace("[SERVER_NAME]", f"{client.custom_domain} www.{client.custom_domain}" # Altera o server name
                ).replace("[CUSTOM_DOMAIN]", client.custom_domain) # Altera o custom domain
                with open(self.location, "a") as new_file: new_file.write("\n" + new_txt) # Escreve no arquivo atual
                print(f"/home/guibs/panel/venv/bin/certbot certonly --manual -d {client.custom_domain} -d www.{client.custom_domain} -y")
                call(f"/home/guibs/panel/venv/bin/certbot certonly --manual -d {client.custom_domain} -d www.{client.custom_domain} -y") # Gera o certificado do site
                call("systemctl restart nginx") # Reinicia o serviidor
