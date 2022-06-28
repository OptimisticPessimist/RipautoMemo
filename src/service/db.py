from typing import Any

import sqlalchemy
from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import TestConfig as Config
from src.domain import User

DB = Config.db
engine = sqlalchemy.create_engine(DB, echo=True)
Base = declarative_base()


def _create_db() -> None:
    """
    Create DB if nothing it.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)


class Users(Base):  # type: ignore
    """Schema of Users"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(length=40))
    user_name = Column(String(length=1_023))
    nickname = Column(String(length=1_023))
    img_path = Column(String(length=32_768))
    met = Column(Date)
    place = Column(String(length=1_023))
    tags = Column(JSON)
    memo = Column(String(length=10_000))

    __tablename__ = "user"

    @staticmethod
    def insert(data: User) -> None:
        """
        Insert user data.

        Args:
            data: user data

        Returns:
            None
        """
        _create_db()

        session = sessionmaker(bind=engine)()
        info = Users()
        info.uid = data.uid
        info.user_name = data.user_name
        info.nickname = data.nickname
        info.img_path = data.img_path
        info.met = data.met
        info.place = data.place
        info.tags = data.tags
        info.memo = data.memo
        session.add(instance=info)
        session.commit()
        session.close()

    @staticmethod
    def select_all() -> Any:
        """
        Get list of all users data.

        Returns:
            (Any) All users data
        """
        session = sessionmaker(bind=engine)()
        users = session.query(Users)
        session.close()
        return users

    @staticmethod
    def select_by_name(name: str) -> Any:
        """
        Get list of users matching the keyword by name.

        Args:
            name: keyword

        Returns:
            (Any) Users list of matching the keyword
        """
        session = sessionmaker(bind=engine)()
        users = session.query(Users).filter(Users.user_name.like(f"%{name}%") | Users.nickname.like(f"%{name}%"))
        session.close()
        return users

    @staticmethod
    def select_by_tag(tag: str | bytes) -> Any:
        """
        Get list of users matching the keyword by name.

        Args:
            tag: keyword

        Returns:
            (Any) Users list of matching the keyword
        """
        session = sessionmaker(bind=engine)()
        users = session.query(Users).filter(Users.tags.like(f"%{tag}%"))
        session.close()
        return users

    @staticmethod
    def delete_by_id(id_: str) -> None:
        """
        Delete user having the id.

        Args:
            id_: id in DB

        Returns:
            None
        """
        session = sessionmaker(bind=engine)()
        target = session.query(Users).filter_by(Users.id == id_).one()
        session.delete(target)
        session.commit()
        session.close()

    @staticmethod
    def update_by_id(id_: str, data: User) -> None:
        """
        Update user data.

        Args:
            id_: id in DB
            data: User data

        Returns:
            (None)
        """
        session = sessionmaker(bind=engine)()
        user = session.query(Users).filter(Users.id == id_).first()
        user.uid = data.uid
        user.user_name = data.user_name
        user.nickname = data.nickname
        user.img_path = data.img_path
        user.met = data.met
        user.place = data.place
        user.tags = data.tags
        user.memo = data.memo
        session.commit()
        session.close()

    @staticmethod
    def select_by_id(id_: int) -> Any:
        """

        Args:
            id_:

        Returns:

        """
        session = sessionmaker(bind=engine)()
        target = session.query(Users).filter(Users.id == id_).one()
        session.close()
        target.met = str(target.met)
        return target
