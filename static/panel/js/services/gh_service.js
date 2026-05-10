import { ApiRequest } from "../utils/request.js"
import { api } from "../utils/env.js"

const id = window.location.pathname.replace("/client/", "")
const req = await new ApiRequest(`/eventos/gh/${id}`).send()
const res = await req.json()
const commit_comment = res[0]["commit"]["message"]
const commit_date = new Date(res[0]["commit"]["author"]["date"]).toLocaleDateString("pt-br", {day:"2-digit", month:"2-digit", year:"numeric", hour:"2-digit", minute:"2-digit"})
const commit_author = res[0]["commit"]["author"]["name"]

document.querySelectorAll("[data-set]").forEach(async(el) => {
    if(req.ok){
        switch(el.dataset.set){
            case "commit-comment":
                return el.textContent = commit_comment
            case "commit-date":
                return el.textContent = commit_date

            case "commit-author":
                return el.textContent = commit_author
        };
    };
});