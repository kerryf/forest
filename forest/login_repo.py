from typing import Optional

from forest.db import get_db


def record_action(data: dict) -> None:
    sql = '''insert into login (person_id, action, ip_address, user_agent, created_at) 
    values (?, ?, ?, ?, CURRENT_TIMESTAMP)
    '''

    db = get_db()
    db.execute(sql, (data['person_id'], data['action'], data['ip_address'], data['user_agent']))

    return None
