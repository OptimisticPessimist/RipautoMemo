from pathlib import Path
from typing import Any

from src.domain import User

from .service.db import Users
from .service.watch import FriendLog, Scraper


def _prepare_user(data: dict[str, str]) -> User:
    """
    Prepare user data.

    Args:
        data: dictionary of User data

    Returns:
        (User) User data
    """
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
    def create_user(data: dict[str, str]) -> None:
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
        """

        Args:
            id_:
            data:

        Returns:

        """
        user = _prepare_user(data)
        if data["img_path"] == "":
            user.img_path = Controller.read_by_id(id_)["img_path"]
        Users.update_by_id(id_, user)

    @staticmethod
    def delete_user(id_: str) -> None:
        """

        Args:
            id_:

        Returns:

        """
        Users.delete_by_id(id_)

    @staticmethod
    def delete_uid(uid: str) -> None:
        Users.delete_by_uid(uid)

    @staticmethod
    def result(users: list[Users]) -> list[Any]:
        """

        Args:
            users:

        Returns:

        """
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
    def read_all_user() -> list[Any]:
        """
        Search all friend from DB.

        Returns:
            (list) [image path, user name, nickname, [tag1, tag2, tag3, tag4, tag5]]
        """
        users = Users.read_all()
        return Controller.result(users)

    @staticmethod
    def read_by_name(name: str) -> list[Any]:
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
    def read_by_tag(tag: str) -> list[Any]:
        """

        Args:
            tag:

        Returns:

        """
        tag = tag.encode("unicode-escape").decode("ascii")
        users = Users.read_by_tag(tag)
        return Controller.result(users)

    @staticmethod
    def read_by_id(id_: str) -> dict[str, str | Path]:
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

    @staticmethod
    def read_by_uid(uid: str) -> Any:
        user = Users.read_by_uid(uid)
        return user


class AutoRegister:
    def __init__(self) -> None:
        self.friend_logs = FriendLog()

    def analysis(self) -> list[dict[str, str]]:
        friends = self.friend_logs.analysis()
        data = list()
        for friend in friends:
            if not Controller.read_by_uid(friend.uid):
                datum = dict(
                    uid=friend.uid,
                    user_name=friend.username,
                    nickname="",
                    img_path="",
                    met=friend.date,
                    place=friend.world,
                    tag1="auto-writing",
                    tag2="",
                    tag3="",
                    tag4="",
                    tag5="",
                    memo="",
                )
                data.append(datum)
        return data


class FriendsList:
    def __init__(self) -> None:
        self.scraper = Scraper()

    def get(self, username: str, password: str) -> None:
        friends = self.scraper.get(username, password)
        tmp = dict(
            uid="temporally user",
            user_name="Jon Doe",
            nickname="",
            img_path="",
            met="2017-02-01",
            place="",
            tag1="temporally user",
            tag2="",
            tag3="",
            tag4="",
            tag5="",
            memo="",
        )
        Controller.create_user(tmp)
        for friend in friends:
            if Users.read_by_uid(friend[1]):
                continue
            datum = dict(
                uid=friend[1],
                user_name=friend[0],
                nickname="",
                img_path="",
                met="2017-02-01",
                place="",
                tag1="auto-writing",
                tag2="",
                tag3="",
                tag4="",
                tag5="",
                memo="",
            )
            Controller.create_user(datum)
        Controller.delete_uid("temporally user")
