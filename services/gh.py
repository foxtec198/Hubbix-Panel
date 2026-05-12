from os import getenv
from requests import get
from functools import cache
from datetime import datetime as dt
from models.clients import Client, db

class GitHub:
    TOKEN = getenv("GH_TOKEN")
    OWNER = getenv("OWNER")
    REPO = getenv("REPO")
    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"

    def _get_last_commit(self, path: str, per_page: int = 1):
        url = f"{self.URL}?path={path}&per_page={per_page}"
        headers={"Authorization": f"Bearer {self.TOKEN}", "Accept": "application/vnd.github+json"}
        response = get(url, headers=headers)
        response.raise_for_status()
        data = response.json()[0]
        commit_date = (
            data
            .get("commit", {})
            .get("author", {})
            .get("date")
        )

        if not commit_date: return None
        return {"data": data, "date": dt.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")}

    @cache
    def get_commits(self, client: Client):
        if not client: return None # Caso nao encontre o cliente
        template_commit = self._get_last_commit(f"templates/clients/{client.template}") # Commits do template (HTML)
        static_commit = self._get_last_commit(f"static/{client.template}") # Commits do Static (CSS/JS/JSON/IMGS)

        # Caso encontre os dois confirma qual é mais recente e retorna o mesmo
        last_commmit =  max([template_commit, static_commit], key=lambda x: x["date"])["data"]
        if not last_commmit: return None # Caso nao encontre

        now_sha = last_commmit.get("sha")
        last_sha = client.gh_sha
        if now_sha == last_sha: return None

        author = last_commmit.get("commit").get("author")
        message = last_commmit.get("commit").get("message")
        date = dt.strptime(author.get("date"), "%Y-%m-%dT%H:%M:%SZ")

        client.gh_sha = now_sha
        client.gh_commit = message
        client.gh_author = author.get("name")
        client.gh_date = date
        db.session.commit()
