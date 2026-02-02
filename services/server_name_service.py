from models.client import Client
from os import path, getcwd, mkdir
from subprocess import call

class Server:
    def normalize_domain(self, domain:str):
        return domain.replace(".com.br", "").replace(".com", "").replace(".live", "").replace('.shop', "")

    def config_domain(self, client: Client) -> None:
        filename = f"/etc/nginx/sites-avaible/{client.custom_domain}"
        if client.custom_domain and not path.exists(filename):
            sh = f"""
            #!/bin/bash
            echo '84584608' | echo '' > /etc/nginx/sites-avaible/{self.normalize_domainn(client.custom_domain)}
            """
            call(sh)