function calculate() {
    var x = document.getElementById("current").innerHTML.slice(1)
    var y = document.getElementById("spent").innerHTML.slice(1)
    var z = x - y
    document.getElementById("result").innerHTML = "$" + z;
}

const openFormButtons = document.querySelectorAll('[data-form-target]')
const closeFormButtons = document.querySelectorAll('[data-close-button]')
const submitFormButtons = document.querySelectorAll('[data-submit-button]')
const overlay = document.getElementById('overlay')

openFormButtons.forEach(button => {
    button.addEventListener('click', () => {
        const form = document.querySelector(button.dataset.formTarget)
        openForm(form)
    })
})

closeFormButtons.forEach(button => {
    button.addEventListener('click', () => {
        const form = button.closest('.form')
        closeForm(form)
    })
})

function openForm(form) {
    if (form == null) return
    form.classList.add('active')
    overlay.classList.add('active')
}

function closeForm(form) {
    if (form == null) return
    form.classList.remove('active')
    overlay.classList.remove('active')
}