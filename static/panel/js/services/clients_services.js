import { offcanvas, show_toast, clear_number } from "../utils/ui.js"
import { Client } from "../models/clients_models.js"
import { ApiRequest } from "../utils/request.js";

function createClientCard(data) {
    const card = document.createElement("div");
    card.className = "d-flex flex-grow-1 flex-column gap-2 border glass p-4 rounded-4";
    card.style.maxWidth = "450px"
    card.style.minWidth = "450px"

    // HEADER
    const header = document.createElement("div");
    header.className = "d-flex gap-3 align-items-center";

    // LOGO WRAPPER
    const logoWrapper = document.createElement("div");
    logoWrapper.className = "d-flex neon-border justify-content-center bg-gray rounded-4 align-items-center p-2";

    const logo = document.createElement("img");
    logo.src = data.logo;
    logo.alt = "client_brand";
    logo.width = 60;
    logo.height = 60;
    logo.className = "img-fluid bg-gray object-fit-contain";
    logo.style.width = "5vw";
    logo.style.height = "5vh";

    logoWrapper.appendChild(logo);

    // INFO
    const info = document.createElement("div");
    info.className = "d-flex flex-grow-1 flex-column";

    const title = document.createElement("span");
    title.className = "fw-bold text-primary";
    title.textContent = data.name;

    const domain = document.createElement("span");
    domain.className = "tiny-text text-secondary";
    domain.textContent = data.domain;

    info.appendChild(title);
    info.appendChild(domain);

    // STATUS
    const statusWrapper = document.createElement("div");
    statusWrapper.className = "d-flex";

    const status = document.createElement("span");
    status.className = `badge fs-6 rounded-pill glass ${data.statusClass}`;
    status.textContent = data.status;

    statusWrapper.appendChild(status);

    // HEADER APPEND
    header.appendChild(logoWrapper);
    header.appendChild(info);
    header.appendChild(statusWrapper);

    // HR
    const hr = document.createElement("hr");

    // FOOTER
    const footer = document.createElement("div");
    footer.className = "d-flex justify-content-between";

    // ACTIONS
    const actions = document.createElement("div");
    actions.className = "d-flex gap-2";

    const buttons = [
        {
            icon: "bi-eye",
            class: "btn-outline-success",
            onClick: data.onView
        },
        {
            icon: "bi-github",
            class: "btn-outline-success",
            onClick: data.onGithub
        },
        {
            icon: "bi-bar-chart-line",
            class: "btn-outline-success",
            onClick: data.onAnalytics
        }
    ];

    buttons.forEach(btnData => {
        const button = document.createElement("button");
        button.className = `btn ${btnData.class}`;

        const icon = document.createElement("i");
        icon.className = `bi ${btnData.icon}`;

        button.appendChild(icon);

        if (btnData.onClick) {
            button.addEventListener("click", btnData.onClick);
        }

        actions.appendChild(button);
    });

    // MANAGE BUTTON
    const manageWrapper = document.createElement("div");
    manageWrapper.className = "d-flex";

    const manageButton = document.createElement("button");
    manageButton.className = "btn btn-outline-success";
    manageButton.textContent = "Gerenciar >";

    if (data.onManage) {
        manageButton.addEventListener("click", data.onManage);
    }

    manageWrapper.appendChild(manageButton);

    // FOOTER APPEND
    footer.appendChild(actions);
    footer.appendChild(manageWrapper);

    // CARD APPEND
    card.appendChild(header);
    card.appendChild(hr);
    card.appendChild(footer);

    return card;
}

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
    const list_of_clients = document.querySelector("[data-set='list_clients']")
    const infos = clients.infos // Obtem as infos (Calculadas no servidor )
    const isLocalHost = window.location.hostname.includes("localhost")
    
    infos["ativos"] = 0 // Adiciona os ativos como 0
    infos["inativos"] = 0 // Adiciona os inativos como 0
    infos["total"] = clients.results.length // Adiciona o total de clientes as infos

    // Loop para cada cliente
    clients.results.forEach(client => {
        client.active ? infos["ativos"] += 1 : infos["inativos"] += 1 //  Seta ativo ou inativo nas infos
        const logo = client.logo == "blank.png" 
            ? "https://api.hubbix.com.br/img/blank.png"
            : `/static/${client.template}/img/${client.logo}`

        const domain = client.custom_domain 
            ? client.custom_domain : 
                isLocalHost 
                    ? client.subdomain + ".localhost:5000"
                    : client.subdomain + ".lp.hubbix.com.br"
        
        const link = domain.includes("localhost") ? "http://" + domain : "https://" + domain
        
        const card = createClientCard({
            logo: logo,
            name: client.name,
            domain: domain,
            status: client.active ? "Ativo" : "Offline",
            statusClass: client.active ? "bg-outline-primary" : "bg-outline-red",

            onView: () => {
                window.open(link, "_blank")
            },

            onGithub: () => {
                window.open(`https://github.com/foxtec198/Hubbix-Panel/tree/main/templates/clients/${client.template}`, "_blank")
            },

            onAnalytics: () => {
                console.log("ANALYTICS");
            },

            onManage: () => {
                location = `/client/${client.id}`
            }
        });
        list_of_clients.appendChild(card) // Adiciona o item da lista ao container 
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