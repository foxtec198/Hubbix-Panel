// exampleModal
var spinner = '<span id="spin_ldg" class="spinner-border spinner-border-sm text-light" role="status"></span>'
const email = 'foxtec198@gmail.com' 

document.getElementById('form').addEventListener('submit', async function (e){
    e.preventDefault()

    nome = this.nome.value
    tel = this.tel.value
    btn = this.btnEmail


    const html = `
        <h1>Você tem um novo pedido!</h1>
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
                "title": `Novo pedido de Visita - ${nome}`,
                "html": html
            })
        }
    )
    const res = await req.json()
    const el_toast = document.getElementById("toast")
    const toast = bootstrap.Toast.getOrCreateInstance(el_toast) 
    toast.show()
    if(req.ok){btn.innerHTML = res}
})