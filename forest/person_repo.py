from typing import Optional

from werkzeug.security import generate_password_hash

from forest.db import get_db


def create_person(data: dict) -> int:
    sql = '''insert into person (name, email, password, mobile, enabled, locked, change_password, created_at) 
    values (?, ?, ?, ?, 1, 0, 0, CURRENT_TIMESTAMP)
    '''

    password = generate_password_hash(data['password'], method='pbkdf2:sha512')

    db = get_db()
    db.execute(sql, (data['name'], data['email'], password, data['mobile'], data['change_password']))
    person_id = db.cursor().lastrowid

    return person_id


def get_person(person_id: int) -> Optional[dict]:
    db = get_db()
    person = db.execute('select * from person where id = ?', (person_id,)).fetchone()

    return person


def find_person(email: str) -> Optional[dict]:
    db = get_db()
    person = db.execute('select * from person where email = ?', (email,)).fetchone()

    return person
