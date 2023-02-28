from typing import Optional

from flask import get_flashed_messages


def dart_has(key: str) -> bool:
    # Returns true if a message exists for key
    return len(get_flashed_messages(False, key)) > 0


def dart_first(key: str) -> Optional[str]:
    # Returns the first message for key, or None
    messages = get_flashed_messages(False, key)
    if len(messages) > 0:
        message = messages[0]
    else:
        message = None

    return message
