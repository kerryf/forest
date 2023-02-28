from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from forest.guard import generate_csrf_token, guest_required, login_required
from forest.person_repo import find_person

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
@guest_required
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # TODO: validate form data

        error = None
        person = find_person(email)

        if person is None:
            error = 'Incorrect username'
        elif not check_password_hash(person['password'], password):
            error = 'Incorrect password'

        # TODO: check enabled, locked, and csrf token

        if error is None:
            session.clear()
            session['forest_person'] = person['id']
            generate_csrf_token()
            return redirect(url_for('home.index'))

        flash(error, 'login_error')
    else:
        generate_csrf_token()

    return render_template('login.html')


@bp.post('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('forest.index'))
