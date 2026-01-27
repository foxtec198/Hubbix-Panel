document.addEventListener('scroll', function() {
    const background = document.querySelector('.backHero');
    const content = document.querySelector('.contHero');
    const scrollPosition = window.scrollY;
    const contentTop = content.offsetTop;

    if (scrollPosition >= contentTop) {
        background.style.position = 'fixed';
        background.style.top = '0';
    } else {
        background.style.position = 'absolute';
        background.style.top = '0';
    }
});