// JavaScript para interações simples
document.addEventListener('DOMContentLoaded', function() {
    // Validação básica do formulário de contato
    const contactForm = document.getElementById('contactForm');
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();
        alert('Obrigado! Sua mensagem foi enviada. Entraremos em contato em breve.');
        contactForm.reset();
    });

    // Smooth scroll para links de navegação
    const navLinks = document.querySelectorAll('.navbar-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
});