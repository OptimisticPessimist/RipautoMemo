from typing import Any

import sqlalchemy
from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import Config
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


def _write_user(data: User, target: User) -> User:
    """
    Replace user data for preparing write DB.

    Args:
        data: new data
        target: old data

    Returns:
        (User) new data
    """
    target.uid = data.uid
    target.user_name = data.user_name
    target.nickname = data.nickname
    target.img_path = data.img_path
    target.met = data.met
    target.place = data.place
    target.tags = data.tags
    target.memo = data.memo
    return target


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
    def create_user(data: User) -> None:
        """
        Insert user data.

        Args:
            data: user data

        Returns:
            None
        """
        _create_db()

        session = sessionmaker(bind=engine)()
        info = _write_user(data, Users())
        session.add(instance=info)
        session.commit()
        session.close()

    @staticmethod
    def read_all() -> Any:
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
    def read_by_name(name: str) -> Any:
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
    def select_by_tag(tag: str) -> Any:
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
        target = session.query(Users).filter(Users.id == id_).one()
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
        _write_user(data, session.query(Users).filter(Users.id == id_).first())
        session.commit()
        session.close()

    @staticmethod
    def read_by_id(id_: int) -> Any:
        """

        Args:
            id_: ID of DB

        Returns:
            user datum
        """
        session = sessionmaker(bind=engine)()
        target = session.query(Users).filter(Users.id == id_).one()
        session.close()
        target.met = str(target.met)
        return target
