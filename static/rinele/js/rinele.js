// exampleModal
var spinner = '<span id="spin_ldg" class="spinner-border spinner-border-sm text-light" role="status"></span>'
const email = 'foxtec198@gmail.com' 

function create_modal(id, title, body, center='modal-dialog-centered', backdrop='static'){
    container = document.createElement('div')
    const modalHtml = `
        <div class="modal text-dark fade" id="${id}" tabindex="-1" aria-labelledby="modalLabel" data-bs-backdrop="false" aria-hidden="true">
            <div class="modal-dialog ${center}">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                </div>
                <div class="modal-body">
                    ${body}
                </div>
            </div>
            </div>
        </div>
    `;
    container.innerHTML = modalHtml
    document.body.appendChild(container)
    return new bootstrap.Modal(document.getElementById(id), {'show':true, 'backdrop': backdrop})
}

document.getElementById('form').addEventListener('submit', async function (e){
    e.preventDefault()

    nome = document.getElementById('nome').value
    tel = document.getElementById('tel').value
    btn = document.getElementById('btnEmail')

    const html = `
        <h1>Você tem uma nova capitação!</h1>
        <p>Entre em contato para mais detalhes!</p>
        <hr>
        <br>
        <p><strong>Nome: </strong>${nome}</p>
        <p><strong>Telefone: </strong>${tel}</p>
        <a style="background: #5E8B60; color: #fff; padding: 8px; border-radius: 8px; width: 100%;" href="https://wa.me/${tel}">Enviar mensagem no WhatsApp!</a>
        <br>
        <br>
        <hr>
        <a style="color: #5E8B60; text-decoration: none;" href="https://tecnobreve.onrender.com">© Desenvolvido por Tecnobreve, 2025</a>
        `

    btn.innerHTML = spinner
    const req = await fetch(
        `https://api.hubbix.com.br/send_mail/${email}`, 
        {
            method: 'POST', 
            headers: {"Content-Type": "application/json"}, 
            body: JSON.stringify({
                "title": `Nova capitação - ${nome}`,
                "html": html
            })
        }
    )
    const res = await req.json()
    create_modal('modal3', '<i class="bi bi-envelope-fill"></i> Envio de email', res, null, true).show()
    if(req.ok){btn.innerHTML = res}
    
})