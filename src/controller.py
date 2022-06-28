from typing import Any

from src.domain import User

from .service.db import Users


def _prepare_user(data: dict[str, str]) -> User:
    user = User(
        uid=data["uid"],
        user_name=data["user_name"],
        nickname=data["nickname"],
        img_path=data["img_path"],
        met=data["met"],
        place=data["place"],
        t1=data["tag1"],
        t2=data["tag2"],
        t3=data["tag3"],
        t4=data["tag4"],
        t5=data["tag5"],
        memo=data["memo"],
    )
    return user


class Controller:
    @staticmethod
    def insert_user(data: dict[str, str]) -> None:
        """
        Insert data to DB.

        Args:
            data: input data by HTML

        Returns:
            None
        """
        user = _prepare_user(data)
        Users.create_user(user)

    @staticmethod
    def update_user(id_: str, data: dict[str, str]) -> None:
        user = _prepare_user(data)
        Users.update_by_id(id_, user)

    @staticmethod
    def result(users: list[Users]) -> list[Any]:
        result = list()
        for user in users:
            id_ = user.id
            img_path = user.img_path
            user_name = user.user_name
            nickname = user.nickname
            tags = user.tags
            result.append([id_, img_path, user_name, nickname, tags])
        return result

    @staticmethod
    def select_all_db() -> list[Any]:
        """
        Search all friend from DB.

        Returns:
            (list) [image path, user name, nickname, [tag1, tag2, tag3, tag4, tag5]]
        """
        users = Users.read_all()
        return Controller.result(users)

    @staticmethod
    def select_by_name(name: str) -> list[Any]:
        """
        Search keyword in names from DB.

        Args:
            name: keyword

        Returns:
            {
                "id": id
                "img_path": image path,
                "user_name": user name,
                "nickname": nickname,
                "tags": [tag1, tag2, tag3, tag4, tag5],
            }
        """
        users = Users.read_by_name(name)
        return Controller.result(users)

    @staticmethod
    def select_by_tag(tag: str) -> list[Any]:
        tag = tag.encode("unicode-escape").decode("ascii")
        users = Users.select_by_tag(tag)
        return Controller.result(users)

    @staticmethod
    def select_by_id(id_: str) -> dict[str, str | list[str]]:
        """

        Args:
            id_:

        Returns:

        """
        user = Users.read_by_id(int(id_))
        result = dict()
        result["img_path"] = user.img_path
        result["user_name"] = user.user_name
        result["nickname"] = user.nickname
        result["met"] = user.met
        result["place"] = user.place
        result["tags"] = user.tags
        result["uid"] = user.uid
        result["memo"] = user.memo
        return result
