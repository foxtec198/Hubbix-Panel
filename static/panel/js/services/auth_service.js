import { api } from "../utils/env.js"
import { is_loading, show_toast } from "../utils/ui.js"

const form_login = document.getElementById("form-login") // Evento de Login
form_login ? form_login.addEventListener("submit", async(e)=>{
    e.preventDefault();
    is_loading();
    const form = new FormData(form_login);
    let req;
    try{req = await fetch(api + "/config/login", { method: "POST", body: form });}
    catch{is_loading(false); show_toast("Erro na conexão com o servidor! Tente novamente mais tarde.", "danger"); return};

    const res = await req.json();
    
    if(req.ok){
        sessionStorage.setItem("access_token", res.access_token);
        sessionStorage.setItem("display_name", res.display_name);
        sessionStorage.setItem("email", res.email);
        window.location.href = "/home";
    }else{ is_loading(false); show_toast(res, "danger"); };
}) : null;