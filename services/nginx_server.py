from models.client import Client
from os import path, getcwd

class NginxServer():
    model_filename = path.join(getcwd(), "models", "nginx_model.conf")
    location = path.join("etc", "nginx", "sites-available", "panel.conf")

    def config(self, client:Client):
        with open(self.model_filename, "r", encoding="utf-8") as file: default = file.read() # Le os dados do MODELO do Nginx (Com HTTPS)
        new_txt = default.replace("[CLIENT_ID]", client.name.upper() # Altera o nome de identificação
        ).replace("[SERVER_NAME]", f"{client.custom_domain} www.{client.custom_domain}" # Altera o server name
        ).replace("[CUSTOM_DOMAIN]", client.custom_domain) # Altera o custom domain
        with open(self.location, "r") as new_file: file = new_file.read()
        if not file.__contains__(client.custom_domain):
            with open(self.location, "a") as new_file: new_file.write("\n" + new_txt) # Escreve no arquivo atual
            return "Dominio configurado com sucesso"