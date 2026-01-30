function alter_active(self){
    let elements = document.querySelectorAll('.nav-link');
    elements.forEach((element) => {
        element.classList.remove('active');
    });
    self.classList.add('active');
}