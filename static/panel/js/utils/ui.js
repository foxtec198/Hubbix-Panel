import { img } from "../utils/env.js"

export const offcanvas = document.getElementById("offcanvasRight") ? new bootstrap.Offcanvas(document.getElementById("offcanvasRight")) : null;
const div = document.createElement("div");
const divLdg = document.createElement("div");
const options = `<div id="manager_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true"> <div class="toast-header"> <img src="${img}" width="20vh" class="rounded me-2" alt="logo"> <strong class="me-auto" id="toast_title"></strong> <small>Agora.</small> <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button> </div> <div class="toast-body" id="toast_msg"></div> </div>`;
div.classList.add("toast-container", "position-fixed", "bottom-0", "end-0", "p-3");
div.innerHTML = options;
parent.document.body.appendChild(div);

export function show_toast(msg, type = "info"){
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

export function is_loading(state=true) {
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
        divLdg.innerHTML = `<div class="loader"> <div class="loader-square"></div> <div class="loader-square"></div> <div class="loader-square"></div> <div class="loader-square"></div> <div class="loader-square"></div> <div class="loader-square"></div> <div class="loader-square"></div> </div>`;
        parent.document.body.appendChild(divLdg);
    } else { 
        divLdg.hidden = 'none' 
        try{ document.body.removeChild(divLdg); } catch{ return };
    };
};

export function logout(){
    document.cookie = "access_token=; path=/; max-age=0;"
    sessionStorage.clear()
    location = "/"
};

export function clear_number(str){
    return str
        .replaceAll("_", "")
        .replaceAll("(", "")
        .replaceAll(")", "")
        .replaceAll("-", "")
        .replaceAll(".", "")
        .replaceAll(",", "")
        .replaceAll(" ", "")
        .trim()
}