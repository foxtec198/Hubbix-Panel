from os import getenv
from requests import get
from functools import cache
from datetime import datetime as dt
from models.clients import Client

class GitHub:
    TOKEN = getenv("GH_TOKEN")
    OWNER = getenv("OWNER")
    REPO = getenv("REPO")
    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"

    @cache
    def get_commits(self, client_id, pagination=1):
        client = Client._search_by_id(int(client_id))
        if client:
            template_name = client.template

            # Customers Templates
            path = f"{self.URL}?path=templates/clients/{template_name}&per_page={pagination}"
            templates = get(path, headers={ "Authorization": f"Bearer {self.TOKEN}", "Accept": "application/vnd.github+json" })
            template_date = templates.json()[0]["commit"]["author"]["date"]
            template_date = dt.strptime(template_date, "%Y-%m-%dT%H:%M:%SZ")

            # Customers Static
            path = f"{self.URL}?path=static/{template_name}&per_page={pagination}"
            static = get(path, headers={ "Authorization": f"Bearer {self.TOKEN}", "Accept": "application/vnd.github+json" })
            static_date = static.json()[0]["commit"]["author"]["date"]
            static_date = dt.strptime(static_date, "%Y-%m-%dT%H:%M:%SZ")

            if template_date > static_date: return templates.json()
            if static_date > template_date: return static.json()
            return templates.json()