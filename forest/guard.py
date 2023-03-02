import functools
import os
from hashlib import sha1
from typing import Optional

from flask import abort, session, redirect, url_for, g

from forest.person_repo import get_person
from forest.role_repo import person_has_role


def generate_csrf_token() -> None:
    # Adds a new token to the session if one does not already exist
    if 'csrf_token' not in session.keys():
        session['csrf_token'] = sha1(os.urandom(64)).hexdigest()

    return None


def csrf_token() -> Optional[str]:
    # Returns the token, if one exists, or None
    if 'csrf_token' in session.keys():
        return session['csrf_token']

    return None


def check_csrf_token(form_token: str) -> None:

    if 'csrf_token' in session.keys():
        session_token = session['csrf_token']
        valid = session_token == form_token
        if not valid:
            abort(403, 'invalid_token')
    else:
        abort(401)

    return None


def has_role(roles: list[str]) -> bool:
    person_id = session.get('forest_person')

    if person_id is None:
        abort(401)

    return person_has_role(person_id, roles)


def load_person() -> None:
    person_id = session.get('forest_person')

    if person_id is None:
        g.person = None
    else:
        g.person = get_person(person_id)

    return None


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


def role_required(roles: list[str]):
    def role_decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):

            authorized = has_role(roles)
            if not authorized:
                abort(403, 'denied')

            return view(**kwargs)

        return wrapped_view
