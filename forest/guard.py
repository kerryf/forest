import functools

from flask import session, redirect, url_for, g

from forest.person_repo import get_person


def load_person():
    person_id = session.get('forest_person')

    if person_id is None:
        g.person = None
    else:
        g.person = get_person(person_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.person is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def guest_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.person is not None:
            return redirect(url_for('home.index'))

        return view(**kwargs)

    return wrapped_view
