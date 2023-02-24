from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from forest.guard import guest_required, login_required
from forest.person_repo import find_person

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
@guest_required
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        person = find_person(username)

        if person is None:
            error = 'Incorrect username.'
        elif not check_password_hash(person['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['forest_person'] = person['id']
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('login.html')


@bp.post('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('forest.index'))
