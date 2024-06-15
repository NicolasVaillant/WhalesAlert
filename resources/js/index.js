const setTextFromParameters = () => {
    Object.entries(settings).forEach(([topKey, topValue]) => {
    const keys = Object.keys(topValue);
    keys.forEach(key => {
        const value = topValue[key];
        const elements = document.querySelectorAll(`.${key}`);
        elements.forEach(element => {
        element.innerHTML = value;
        })
    })
    })
}

const cards = document.querySelectorAll('.card-grid-index');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
        entry.target.style.opacity = 1;
    } else {
        entry.target.style.opacity = 0;
    }
  });
}, {threshold: 0.25});


cards.forEach(card => {
    observer.observe(card);
});

window.onload = function () {
    setTextFromParameters()
    copyrightDate()
}

const copyrightDate = () => {
    const element = document.querySelector('.copyright-date')
    const date = new Date().getFullYear()
    element.innerText = `© ${date}`
}