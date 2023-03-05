// Put your global JavaScript here

/* Expand or collapse navigation on mobile */
u('.navbar-burger').on('click', function () {
    u('.navbar-burger').toggleClass('is-active')
    u('.navbar-menu').toggleClass('is-active')
})

/* Handle the logout link */
u('#logout_link').handle('click', function () {
    u('#logout_form').trigger('submit')
})

/* Enable the delete button on alerts */
u('.notification .delete').on('click', function (e) {
    let child = u(e.target)
    child.parent().remove()
})