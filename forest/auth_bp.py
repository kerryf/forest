from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from forest.guard import check_csrf_token, generate_csrf_token, guest_required, login_required
from forest.person_repo import find_person
from forest.login_repo import record_action

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
@guest_required
def login():
    if request.method == 'POST':
        check_csrf_token(request.form['csrf_token'])

        email = request.form['email']
        password = request.form['password']
        # TODO: validate form data

        error = None
        person = find_person(email)

        if person is None:
            error = 'These credentials do not match our records'
        elif not check_password_hash(person['password'], password):
            error = 'These credentials do not match our records'
        elif person['enabled'] == 0:
            error = 'Your account is disabled. Please contact your system administrator.'

        if error is None:
            # Start with a clean session
            session.clear()
            session['forest_person'] = person['id']
            generate_csrf_token()

            data = {
                'person_id': person['id'],
                'action': 'login',
                'ip_address': request.remote_addr,
                'user_agent': request.user_agent.string
            }
            record_action(data)

            return redirect(url_for('home.index'))

        flash(error, 'login_error')
    else:
        # Establish a 'pre-session' with a csrf token to be used for login requests
        generate_csrf_token()

    return render_template('login.html')


@bp.post('/logout')
@login_required
def logout():

    data = {
        'person_id': session['forest_person'],
        'action': 'logout',
        'ip_address': request.remote_addr,
        'user_agent': request.user_agent.string
    }
    record_action(data)

    session.clear()

    return redirect(url_for('forest.index'))
