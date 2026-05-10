// EVENT SNIPSET FOR WHATSAPP - HUBBIX PANEL
const api = "https://panel.lp.hubbix.com.br/eventos";
const client_id = document.querySelector("[data-info-client]").dataset.infoClient;
const partnership_id = document.querySelector("[data-info-partnership]").dataset.infoPartnership;
const data = {client:{"id":parseInt(client_id),"partnership_id":parseInt(partnership_id)}};

function _setWhatsappClick(){data.type="CLICK";fetch(api,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)})};
function _setView(){data.type="VIEW";fetch(api,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)})};

document.addEventListener("DOMContentLoaded",()=>{_setView()});
document.querySelectorAll("[data-set]").forEach(btn=>{if(btn.dataset.set=="whatsapp-hubbix"){btn.addEventListener("click",_setWhatsappClick)};});