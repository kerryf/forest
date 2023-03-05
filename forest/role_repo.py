from typing import Optional

from forest.db import get_db


def get_role(role_id: int) -> Optional[dict]:
    db = get_db()
    role = db.execute('select * from role where id = ?', (role_id,)).fetchone()

    return role


def find_role(name: str) -> Optional[dict]:
    db = get_db()
    role = db.execute('select * from role where name = ?', (name,)).fetchone()

    return role


def get_person_roles(person_id: int) -> list:
    sql = 'select r.* from role r, person_role pr where r.id = pr.role_id and pr.person_id = ?'

    db = get_db()
    roles = db.execute(sql, (person_id,)).fetchall()

    return roles


def add_person_role(person_id: int, role_id: int) -> None:
    db = get_db()
    db.execute('insert into person_role (person_id, role_id) values (?, ?)', (person_id, role_id))
    db.commit()

    return None


def person_has_role(person_id: int, roles: list[str]) -> bool:
    args = [person_id]
    args.extend(roles)

    select = 'select 1 from role r, person_role pr where r.id = pr.role_id and pr.person_id = ?'
    in_clause = ' and r.name in (%s)' % ','.join('?' for i in roles)

    db = get_db()
    has = db.execute(select + in_clause, args)

    return has is not None
