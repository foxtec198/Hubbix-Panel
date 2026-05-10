import { offcanvas, show_toast, clear_number } from "../utils/ui.js"
import { Client } from "../models/clients_models.js"
import { ApiRequest } from "../utils/request.js";

function create_line_client(client){ // Cria uma linha na lista de clientes
    if(client.id){
        const li = document.createElement("li"); // Cria um list item (MAIN)
        li.classList.add("list-group-item", "list-group-item-action"); // CSS do list item
    
        const divLi = document.createElement("div"); // Div responsavel por dividir os dados dos botoes
        divLi.classList.add("d-flex", "justify-content-between"); // CSS do divLi
    
        const divInfo = document.createElement("div") // Div responsavel pelas dados/infos
        divInfo.classList.add("d-flex", "align-items-center"); // CSS da DivInfo
        divInfo.style.lineHeight = "20px"; // Espaçamento da linha
    
        const divText = document.createElement("div"); // Divião dos textos 
        divText.classList.add("d-flex", "flex-column", "ms-3"); // CSS do divText
    
        const spanIcon = document.createElement("span"); // Icon que será trocado pela logo posteriormente
        spanIcon.classList.add("bi") // CSS do Icone
        client.active ? spanIcon.classList.add("bi-play-circle-fill", "text-primary") 
        : spanIcon.classList.add("bi-pause-circle-fill", "text-danger")
    
        const spanName = document.createElement("span"); // Texto referente ao nome do cliente
        spanName.classList.add("fs-6", "fw-bold"); // CSS do spanname
        spanName.textContent = client.name; // Seta o nome do cliente
    
        const spanDomain = document.createElement("span"); // Span referente ao dominio (Custom/sub)
        spanDomain.classList.add("fs-6", "text-truncate"); // CSS do
        spanDomain.style.maxWidth = "200px"
        const isLocalHost = window.location.hostname.includes("localhost")
    
        // Seta o dominio do vliente
        spanDomain.textContent = client.custom_domain 
            ? client.custom_domain : 
                isLocalHost 
                    ? client.subdomain + ".localhost:5000"
                    : client.subdomain + ".lp.hubbix.com.br"
        
        const btn = document.createElement("button"); 
        btn.classList.add("btn", "btn-sm", "btn-primary", "rounded");
        btn.textContent = "Gerenciar";
    
        btn.dataset.toggle = "offcanvas";
        li.dataset.toggle = "offcanvas";
    
        btn.dataset.bsTarget = "#offcanvasRight";
        li.dataset.bsTarget = "#offcanvasRight";
    
        // Divisao dos textos
        divText.appendChild(spanName);
        divText.appendChild(spanDomain);
    
        // Div de informações
        divInfo.appendChild(spanIcon)
        divInfo.appendChild(divText);
    
        // Divisão principal
        divLi.appendChild(divInfo);
        divLi.appendChild(btn); 
    
        // Abre a pagina de cliente com os dados do mesmo
        const els = [btn, li] // Mesma função para o botao e para o item da lista
        els.forEach(el => { // Percore os elementos e adiciona o evento
            el.addEventListener("click", async() =>{ // Cria o evento de click
                window.location = `/client/${client.id}` // Leva pra pagina de cliente
            });
        }); 
        
        li.appendChild(divLi); // Adiciona os dados ao item da lista
    
        // Retorna o item da lista
        return li; 
    };
};

const form_new_client = document.getElementById("form_new_client"); // Eventos para criação de cliente
form_new_client ? form_new_client.addEventListener("submit", async(e)=>{
    e.preventDefault(); // Evita reload 
    
    const name = form_new_client.name.value
    const domain = form_new_client.sub.value
    const template = form_new_client.template.value

    const req = await new Client()
        .create(name, domain, template)
    const res = await req.json();

    if (req.ok){ show_toast(res); offcanvas.hide();}
}) : null;

export async function get_clients(){
    const req = await new Client().get();
    const clients = await req.json()
    const list_of_clients = document.getElementById("list_of_clients")
    const infos = clients.infos // Obtem as infos (Calculadas no servidor )
    
    list_of_clients.innerHTML = ""
    infos["ativos"] = 0 // Adiciona os ativos como 0
    infos["inativos"] = 0 // Adiciona os inativos como 0
    infos["total"] = clients.results.length // Adiciona o total de clientes as infos

    // Loop para cada cliente
    clients.results.forEach(client => {
        client.active ? infos["ativos"] += 1 : infos["inativos"] += 1 //  Seta ativo ou inativo nas infos
        const li = create_line_client(client) // Cria o item da lista do cliente
        list_of_clients.appendChild(li) // Adiciona o item da lista ao container 
    });

    // Seta os dados dos INFOS e, seis respectivos cards
    document.querySelectorAll("[data-count]").forEach(el => {
        if(el.dataset.count){
            el.textContent = infos[el.dataset.count]
        }
    })
};

document.querySelectorAll("[data-set]").forEach(el => {
    const client_id = parseInt(window.location.pathname.replace("/client/", ""));

    if(el.dataset.set == "client_status"){
        el.addEventListener("change", async(e)=>{
            const req = await new Client().update(client_id, "active", el.checked)
            const res = await req.json()
            if(req.ok){show_toast(res, "info")}
        })
    };

    if(el.dataset.set == "client_custom_domain"){
        el.addEventListener("submit", async(e)=>{
            e.preventDefault();
            const domain = el.querySelector("#domain").value;
            const req = await new Client().update(client_id, "custom", domain);
            const res = await req.json();
            if(req.ok){show_toast(res)};
        });
    };

    if(el.dataset.set == "gtag"){
        el.addEventListener("submit", async(e)=>{
            e.preventDefault(); // Evita reload padrao do forms
            const value = el.querySelector("input").value;
            const req = await new Client().update(client_id, "gtag", value);
            const res = await req.json();
            if(req.ok){show_toast(res)};
        });
    };

    if(el.dataset.set == "pixel"){
        el.addEventListener("submit", async(e)=>{
            e.preventDefault(); // EEvita reload padrao do forms
            const value = el.querySelector("input").value;
            const req = await new Client().update(client_id, "pixel", value);
            const res = await req.json();
            if(req.ok){show_toast(res)};
        });
    };

    if(el.dataset.set == "client_phone"){
        el.addEventListener("submit", async(e)=>{
            e.preventDefault(); //Evita reload padrao do forms
            const tel_input = el.querySelector("#tel");
            const msg = el.querySelector("#msg").value;
            const tel = clear_number(tel_input.value);
            
            if(tel.length >= 10){
                const req = await new Client().update(client_id, "tel", tel, msg)
                const res = await req.json()
                if(req.ok){show_toast(res)}
            }else{show_toast("Numero incorreto preencha corretamente!", "alert")};
        });

    }

    if(el.dataset.set == "remove_client"){
        el.addEventListener("click", async()=>{
            if(confirm("Deseja realmente excluir este cliente permanentemente")){
                const req = await new Client().remove(client_id);
                const res = await req.json();
                if(req.ok){show_toast(res)};
            }
        });
    };
})