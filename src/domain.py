from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class User:
    """User information."""

    uid: str
    user_name: str
    nickname: str
    img_path: str | Path
    met: date
    place: str
    tags: list[str]
    memo: str

    def __init__(
        self,
        uid: str,
        user_name: str,
        nickname: str,
        img_path: str | Path,
        met: str,
        place: str,
        t1: str,
        t2: str,
        t3: str,
        t4: str,
        t5: str,
        memo: str,
    ) -> None:
        """
        Args:
            uid: Unique ID in VRchat Home
            user_name: Name of nameplate at that time.
            nickname: What do you call they?
            img_path: Your friend picture's file path.
            met: Date of they and you met.
            place: In what a world or event did you meet?
            t1: tag1
            t2: tag2
            t3: tag3
            t4: tag4
            t5: tag5
            memo: memo

        Error:
            ValueError: The Date(year, month, day) must be passed correctly.
        """
        self.uid = uid
        self.user_name = user_name
        self.nickname = nickname
        fake_path = "C:\\fakepath\\"
        img_path = str(img_path)
        if fake_path in img_path:
            img_path = img_path.replace(fake_path, "./photo/")
        self.img_path = img_path

        temp: list[str] = met.split("-")
        try:
            year, month, day = int(temp[0]), int(temp[1]), int(temp[2])
            self.met = date(year, month, day)
        except ValueError as e:
            print(f"{e} The Date(year, month, day) must be passed correctly.")

        self.place = place

        self.tags = list()
        tags = [t1, t2, t3, t4, t5]
        tags = sorted(set(tags), key=tags.index)
        if "" in tags:
            tags.remove("")
        if len(tags) == 5:
            self.tags = tags
        else:
            self.tags = list(tags)
            for _ in range(5 - len(self.tags)):
                self.tags.append("")

        self.memo = memo


@dataclass
class Friend:
    username: str
    uid: str
    world: str
    date: str
