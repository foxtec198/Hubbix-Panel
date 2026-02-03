from models.client import Client
from os import path, getcwd

class NginxServer():
    model_filename = path.join(getcwd(), "models", "nginx_model.conf")
    location = path.join("etc", "nginx", "sites-avaible", "panel.conf")

    def __init__(self, client:Client):
        self.client = client
        self.domain = client.custom_domain

    def config(self):
        with open(self.model_filename, "r", encoding="utf-8") as file: default = file.read() # Le os dados do MODELO do Nginx (Com HTTPS)
        new_txt = default.replace("[CLIENT_ID]", self.client.name.upper() # Altera o nome de identificação
        ).replace("[SERVER_NAME]", f"{self.domain} www.{self.domain}" # Altera o server name
        ).replace("[CUSTOM_DOMAIN]", self.domain) # Altera o custom domain
        with open(self.location, "a") as new_file: new_file.write("\n" + new_txt) # Escreve no arquivo atual
        

if __name__ == '_main__':
    new_client = Client(name="Felipe Bertucci", custom_domain="drfelipebertucci.com.br")
    cd = NginxServer(new_client)
    cd.config()
