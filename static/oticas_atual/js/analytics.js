async function __set(type) {
    await fetch('https://api.hubbix.com.br/analytics/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'type': type,
            'unit_id': 1,
            'client_id': 2
        }),
    })
}
// Analytics views
window.addEventListener('load', async function () { __set('VIEW') })

// Analytics clicks
const btns = document.querySelectorAll('#btnAnl')
btns.forEach(item => {
    item.addEventListener('click', async function (e) { __set('CLICK') })
});

// Analytics forms
const forms = document.querySelectorAll('#formAnl')
forms.forEach(item => {
    item.addEventListener('click', async function (e) { __set('FORM') })
});