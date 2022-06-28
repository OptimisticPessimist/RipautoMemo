from typing import Any

import eel

from src.config import TestConfig as Config
from src.controller import Controller


@eel.expose
def insert_db(data: dict[str, str]) -> None:
    """
    Insert data to DB.

    Args:
        data: input data by HTML

    Returns:
        None
    """
    Controller.insert_db(data)


@eel.expose
def select_all_db() -> list[Any]:
    """
    Search all friend from DB.

    Returns:
        (list) [image path, user name, nickname, [tag1, tag2, tag3, tag4, tag5]]
    """
    return Controller.select_all_db()


@eel.expose
def select_by_name_db(name: str) -> Any:
    """
    Search keyword in names from DB.

    Args:
        name: keyword

    Returns:
        (User)
    """
    return Controller.select_by_name_db(name)


@eel.expose
def select_by_tag_db(tag: str) -> Any:
    return Controller.select_by_tag_db(tag)


@eel.expose
def select_by_id_db(id_: str) -> Any:
    return Controller.select_by_id_db(id_)


@eel.expose
def update_by_id_db(id_: str, data: dict[str, str]) -> Any:
    return Controller.update_by_id_db(id_, data)


if __name__ == "__main__":
    eel.init(".")
    eel.start(Config.root, size=Config.monitor_size, port=Config.port, reloader=Config.debug)
