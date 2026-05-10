import { api, img } from "./utils/env.js"
import { get_clients } from "./services/clients_services.js"
import { logout, show_toast } from "./utils/ui.js";

const isHomePage = window.location.pathname == "/home";
const isClientPage = window.location.pathname.includes("/client/");
const socket = io(api);

// Confirma se esta logado
function isAuthenticated() {
    return !!sessionStorage.getItem("access_token");
}

// Confirma se esta na tela de Login
function isLoginPage() {
    const LOGIN_ROUTES = ["/", "/index.html"];
    return LOGIN_ROUTES.includes(window.location.pathname);
};

// Inicia processo de aplicação
async function init() {
    // 🔴 não autenticado → vai pro login
    if (!isAuthenticated() && !isLoginPage()) {
        sessionStorage.clear(); // Limpa o historico de sessão
        parent.window.location.href = "/"; // Força o login
        return; // Inibi continuidade no codigo
    };

    // ✅ Autenticado → vai pra logica
    if (isAuthenticated() && !isLoginPage()) {
        // ================================================ EVENTOS
        document.querySelectorAll("[data-name").forEach(el => {
            const name = el.getAttribute("data-name");
            if (name == "display_name") {
                const first_name = sessionStorage.getItem("display_name").split(" ")[0]
                el.textContent += first_name + ".";
            };
            if (name == "time") {
                const date = new Date();
                const time = date.toLocaleTimeString("pt-br", { hour: "numeric" });
                let msg;
                if (time < 12) { msg = "Bom dia" }
                else if (time >= 12 && time <= 18) { msg = "Boa tarde" }
                else if (time > 18 || time == 0) { msg = "Boa noite" }
                el.textContent = msg
            };
        });

        document.querySelectorAll("[data-set]").forEach(el => {
            if (el.dataset.set == "logout") {
                el.addEventListener("click", () => {
                    logout();
                })
            }
        });

        isHomePage ? get_clients() : null;
        socket.on("update", (data) => {
            switch (data) {
                case "new_client": return isHomePage ? get_clients() : null
                case "client": return isClientPage ? location.reload() : null;
                case "remove_client": return isClientPage ? location = "/home" : null;
            }
        });
    };
}

// INPUTS MASKS
$(document).ready(function () {
    $(".tel-mask").inputmask("(99) 99999-9999");
});

$(document).ready(function () {
    $(".email-mask").inputmask("email");
});

$(document).ready(function () {
    $(".money-mask").inputmask("currency");
});

$(document).ready(function () {
    $(".cpf-mask").inputmask("999.999.999-99");
});

init();