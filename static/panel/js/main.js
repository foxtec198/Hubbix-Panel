var api = "http://panel.localhost:5000"
// var api = "https://lp.hubbix.com.br";

// ================================================ DOM CREATE
const img = "https://api.hubbix.com.br/img/newFav.png"
const div = document.createElement("div")
const divLdg = document.createElement("div")
const options = `<div id="manager_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true"> <div class="toast-header"> <img src="${img}" width="20vh" class="rounded me-2" alt="logo"> <strong class="me-auto" id="toast_title"></strong> <small>Agora.</small> <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button> </div> <div class="toast-body" id="toast_msg"></div> </div>`;
div.classList.add("toast-container", "position-fixed", "bottom-0", "end-0", "p-3");
div.innerHTML = options;
parent.document.body.appendChild(div);
const offcanvas = document.getElementById("offcanvasRight") ? new bootstrap.Offcanvas(document.getElementById("offcanvasRight")) : null;


function create_line_client(client){ // Cria uma linha na lista de clientes
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
    const domain = client.custom_domain ? client.custom_domain : client.subdomain + ".lp.hubbix.com.br"; // Seta o dominio do dliente
    spanDomain.textContent = domain 
    
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
            window.location = `/${client.id}` // Leva pra pagina de cliente
        });
    }); 
    
    li.appendChild(divLi); // Adiciona os dados ao item da lista
    return li; // Retorna o item da lista
};

// ====================================== FUNÇÕES 
function show_toast(msg, type = "info"){
    const manager_toast = parent.document.getElementById('manager_toast');
    const divMsg = parent.document.getElementById("toast_msg");

    if (type == "info") {
        parent.document.getElementById("toast_title").textContent = "Hubbix Manager";
        manager_toast.classList.remove("text-bg-warning", "text-bg-danger");
    } else if (type == "alert") {
        parent.document.getElementById("toast_title").textContent = "Hubbix Manager - Alerta!";
        manager_toast.classList.add("text-bg-warning");
    } else if (type == "danger") {
        parent.document.getElementById("toast_title").textContent = "Hubbix Manager - Antenção!";
        manager_toast.classList.add("text-bg-danger");
    } else {
        console.warn("Tipo de toast não suportado");
        return;
    };

    divMsg.textContent = msg;
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(manager_toast);
    toastBootstrap.show();
};

async function request(url, method = "GET", data = null) {
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

    // Realiza a requisição e retorna a resposta ou erro
    try {
        const req = await fetch(api + url, options);
        const res = await req.json();
        if (req.ok){ is_loading(false); return res; }
        else { is_loading(false); show_toast(res, "danger"); return; };
    }catch(err){
        is_loading(false);
        show_toast("Erro na conexão com o servidor! Tente novamente mais tarde.", "danger");
    }
};

function logout(){
    document.cookie = "access_token=; path=/; max-age=0;"
    window.location = "/"
};

function is_loading(state=true) {
    if (state) {
        divLdg.hidden = '';
        divLdg.style.width = '100%';
        divLdg.style.height = '100%';
        divLdg.style.display = 'flex';
        divLdg.style.justifyContent = 'center';
        divLdg.style.alignItems = 'center';
        divLdg.style.position = 'absolute';
        divLdg.style.zIndex = "5000000000";
        divLdg.style.top = 0;
        // divLdg.style.background = '#2B3035'
        divLdg.innerHTML = `
            <div class="loader">
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            <div class="loader-square"></div>
            </div>`;
        document.body.appendChild(divLdg);
    } else { 
        divLdg.hidden = 'none' 
        try{ document.body.removeChild(divLdg); } catch{ return };
    };
};

// ====================================== EVENTOS 
const form_login = document.getElementById("form-login") // Evento de Login
form_login ? form_login.addEventListener("submit", async(e)=>{
    is_loading();
    e.preventDefault();
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

const form_new_client = document.getElementById("form_new_client"); // Eventos para criação de cliente
form_new_client ? form_new_client.addEventListener("submit", async(e)=>{
    e.preventDefault(); // Evita reload 
    const name = form_new_client.name.value
    const domain = form_new_client.sub.value
    const template = form_new_client.template.value

    is_loading();
    data = { name: name, subdomain: domain };
    template ? data["template"] = template : null;
    const res = await request("/clientes", "POST", data);

    if (res) {
        const li = create_line_client(res.client);
        document.getElementById("list_of_clients").appendChild(li);
        window.location = "/" + res.client.id
    }
}) : null;

document.querySelectorAll("[data-name").forEach(el => {
    const name = el.getAttribute("data-name");
    if (name == "display_name") {
        first_name = sessionStorage.getItem("display_name").split(" ")[0]
        el.textContent += first_name + ".";
    };
    if (name == "time") {
        const date = new Date();
        const time = date.toLocaleTimeString("pt-br", {hour: "numeric"});
        let msg;
        if (time < 12) { msg = "Bom dia"}
        else if (time >= 12 && time <= 18) {msg = "Boa tarde"}
        else if (time > 18 || time == 0) {msg = "Boa noite"}
        el.textContent = msg
    };
})

// ====================================== REQUESTS
async function get_clients(){
    const clients = await request("/clientes");
    
    const infos = clients.infos // Obtem as infos (Calculadas no servidor )
    infos["ativos"] = 0 // Adiciona os ativos como 0
    infos["inativos"] = 0 // Adiciona os inativos como 0
    infos["total"] = clients.results.length // Adiciona o total de clientes as infos

    // Loop para cada cliente
    clients.results.forEach(client => {
        client.active ? infos["ativos"] += 1 : infos["inativos"] += 1 //  Seta ativo ou inativo nas infos
        const li = create_line_client(client) // Cria o item da lista do cliente
        document.getElementById("list_of_clients").appendChild(li) // Adiciona o item da lista ao container 
    });

    // Seta os dados dos INFOS e, seis respectivos cards
    document.querySelectorAll("[data-count]").forEach(el => {
        if(el.dataset.count){
            el.textContent = infos[el.dataset.count]
        }
    })
};