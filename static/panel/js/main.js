var api = "http://panel.localhost:5000"
// var api = "https://panel.lp.hubbix.com.br"
// ================================================ DOM CREATE
const img = "https://api.hubbix.com.br/img/newFav.png"
const div = document.createElement("div")
const options = `
    <div id="manager_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
            <img src="${img}" width="20vh" class="rounded me-2" alt="logo">
            <strong class="me-auto" id="toast_title"></strong>
            <small>now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body" id="toast_msg"></div>
    </div>
`;
div.classList.add("toast-container", "position-fixed", "bottom-0", "end-0", "p-3");
div.innerHTML = options;
parent.document.body.appendChild(div);

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
        parent.document.getElementById("toast_title").textContent = "Hubbix Manager - Perigo!";
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
        Headers: {
            "Content-Type": "application/json",
            "Access-Token": access_token
        }
    };

    // Confere se tem JSON para enviar e se tiver adiciona ao options
    data ? options.body = JSON.stringify(data) : null

    // Realiza a requisiição e retorna a resposta ou erro
    try {
        const req = await fetch(api + url, options);
        const res = await req.json();
        if (req.ok){ return res; }
        else { show_toast(res, "danger"); return; };
    }catch(err){
        show_toast("Erro na conexão com o servidor! Tente novamente mais tarde.", "danger");
    }
};

// ====================================== EVENTOS 
const form_login = document.getElementById("form-login") 
form_login ? form_login.addEventListener("submit", async(e) => {
    e.preventDefault();
    const email = this.email.value;
    const pwd = this.pwd.value;

    const req = await fetch(api + "/config/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "email":email, "password": pwd })
    });
    const res = await req.json()

    if(req.ok){
        document.cookie = `access_token=${res.access_token}; path=/; max-age=3600; expires=0; samesite=strict; secure`;
        sessionStorage.setItem("display_name", res.display_name);
        sessionStorage.setItem("email", res.email);
        window.location.href = "/home";
    }else( show_toast(res, "danger") );

}) : null;

document.querySelectorAll("[data-name").forEach(el => {
    const name = el.getAttribute("data-name");
    if (name == "display_name") {
        el.textContent += sessionStorage.getItem("display_name");
    }
})