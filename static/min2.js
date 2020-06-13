function login_check() {
    var elements = document.getElementsByClassName('input100')
    var email = elements[0]
    var password = elements[1]
    if (email.getAttribute('value') === '') {
        if (email.className.match('has-value')) {
            email.classList.remove('has-val')
        }
    }
    else {
        if (!email.className.match('has-val')) {
            email.classList.add('has-val')
        }
    }
    if (password.getAttribute('value') === '') {
        if (password.className.match('has-val')) {
            password.classList.remove('has-val')
        }
    }
    else {
        if (!password.className.match('has-val')) {
            password.classList.add('has-val')
        }
    }
}
login_check();