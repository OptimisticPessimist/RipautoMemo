import os
from typing import Any

import eel

from src.config import Config
from src.controller import Controller


@eel.expose
def create_user(data: dict[str, str]) -> None:
    """
    Insert data to DB.

    Args:
        data: input data by HTML

    Returns:
        None
    """
    Controller.create_user(data)


@eel.expose
def update_user(id_: str, data: dict[str, str]) -> None:
    Controller.update_user(id_, data)


@eel.expose
def delete_user(id_: str) -> None:
    Controller.delete_user(id_)


@eel.expose
def read_all_user() -> list[Any]:
    """
    Search all friend from DB.

    Returns:
        (list) [image path, user name, nickname, [tag1, tag2, tag3, tag4, tag5]]
    """
    return Controller.read_all_user()


@eel.expose
def read_by_name(name: str) -> Any:
    """
    Search keyword in names from DB.

    Args:
        name: keyword

    Returns:
        (User)
    """
    return Controller.read_by_name(name)


@eel.expose
def read_by_tag(tag: str) -> Any:
    return Controller.read_by_tag(tag)


@eel.expose
def raed_by_id(id_: str) -> Any:
    return Controller.read_by_id(id_)


if __name__ == "__main__":
    new_path = "photo"
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    eel.init(".")
    eel.start(Config.root, size=Config.monitor_size, port=Config.port, reloader=Config.debug)
