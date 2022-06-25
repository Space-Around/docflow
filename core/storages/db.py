import config
import consts

import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (
    String,
    Integer,
    Column,
    Boolean,
    create_engine,
    func,
    exc
)

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'users'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    username = Column('username', String(200), unique=True)
    password = Column('password', String(200), unique=True)
    key = Column('key', String(200), unique=True)
    role = Column('role', Integer())
    is_block = Column('is_block', Integer())

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', password='{self.password}, key='{self.key}', " \
               f"'role='{self.role}', is_block='{self.is_block}')>"


class SessionTable(Base):
    __tablename__ = 'session'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    username = Column('username', String(200))
    token = Column('token', String(200), unique=True)
    ttl = Column('ttl', Integer())

    def __repr__(self):
        return f"<Session(id='{self.id}', username='{self.username}', token='{self.token}, ttl='{self.ttl}')>"


class StorageORM:
    def __init__(self):
        # create connection
        self.engine = create_engine(config.SQLITE_PATH)

        # create tables
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class User:
    __session__ = None

    @classmethod
    def set_session(cls, session):
        cls.__session__ = session

    @classmethod
    def get_by_username(cls, username=''):
        try:
            return cls.__session__.query(UserTable).filter_by(username=username).one()
        except sqlalchemy.exc.NoResultFound:
            pass

        return None

    @classmethod
    def get_by_username_and_password(cls, username='', password=''):
        try:
            return cls.__session__.query(UserTable).filter_by(username=username, password=password).one()
        except sqlalchemy.exc.NoResultFound:
            pass

        return None

    @classmethod
    def get_all(cls):
        try:
            return cls.__session__.query(UserTable).all()
        except sqlalchemy.exc.NoResultFound:
            pass

        return None

    @classmethod
    def add(cls, username='', password='', key=''):
        try:
            user = UserTable(
                username=username,
                password=password,
                key=key,
                role=consts.ROLE_USER,
                is_block=consts.USER_NON_BLOCK
            )

            cls.__session__.add(user)
            cls.__session__.commit()

            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False

    @classmethod
    def block_update(cls, username='', is_block=consts.USER_NON_BLOCK):
        try:
            cls.__session__.query(UserTable).filter_by(username=username).update({'is_block': is_block})
            cls.__session__.commit()
            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False


class Session:
    __session__ = None

    @classmethod
    def set_session(cls, session):
        cls.__session__ = session

    @classmethod
    def add(cls, username='', token='', ttl=''):
        try:
            sess = SessionTable(username=username, token=token, ttl=ttl)

            cls.__session__.add(sess)
            cls.__session__.commit()

            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False

    @classmethod
    def update(cls, username='', token='', ttl=''):
        try:
            cls.__session__.query(SessionTable).filter_by(username=username).update({'token': token, 'ttl': ttl})
            cls.__session__.commit()
            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False

    @classmethod
    def get(cls, token=''):
        try:
            return cls.__session__.query(SessionTable).filter_by(token=token).one()
        except sqlalchemy.exc.NoResultFound:
            pass

        return None

    @classmethod
    def delete(cls, token=''):
        try:
            cls.__session__.query(SessionTable).filter_by(token=token).delete()
            cls.__session__.commit()
            return True
        except sqlalchemy.exc.NoResultFound:
            pass

        return False