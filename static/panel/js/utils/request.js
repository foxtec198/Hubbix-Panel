import { is_loading, show_toast } from "../utils/ui.js"
import { api } from "../utils/env.js"

export class ApiRequest{
    constructor(url, method = "GET", data = null, loading=true){
        // Options para a requisição utilizando o access token, necessário estar logado
        const options = {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Access-Token": sessionStorage.getItem("access_token"),
            }
        };

        // Confere se tem JSON para enviar e se tiver adiciona ao options
        data ? options.body = JSON.stringify(data) : null

        self.url = url
        self.options = options
        self.loading = loading
    };

    async send(){    
        // Realiza a requisição e retorna a resposta ou erro
        is_loading(self.loading);
        const req = await fetch(api + self.url, options);
        if (req.ok){ is_loading(false); return req; }
        else { is_loading(false); show_toast("Erro na requisição, tente novamente mais tarde!", "danger"); return; };
    };
};