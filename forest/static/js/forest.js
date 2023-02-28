// Put your global JavaScript here

u('#logout_link').on('click', function(e) {
    e.preventDefault()
    u('#logout_form').trigger('submit')
})
