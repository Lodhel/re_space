from sqlalchemy import create_engine, Integer
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session
from sqlalchemy.schema import Table, MetaData
from sqlalchemy_utils import EmailType


class Main:

    def create_engine(self):
        return create_engine(
            "postgresql://postgres:q319546@localhost/re_space",
            isolation_level="READ UNCOMMITTED"
        )

    def create_base(self):
        connection = self.create_engine().connect()
        connection.execution_options(
            isolation_level="READ COMMITTED"
        )

        return declarative_base()

    def create_metadata(self):
        return MetaData(bind=self.create_engine())


Base = Main().create_base()
SESSION = create_session(bind=Main().create_engine())


class BaseUser(Base):

    def __init__(self, id=None, email=None, password=None, token=None):
        self.id = id
        self.email = email
        self.password = password
        self.token = token

    __tablename__ = Table('base_user', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(EmailType, unique=True)
    password = Column()
    token = Column()


class Profile(Base):

    def __init__(
            self,
            id=None, user=None, first_name=None, date_join=None,
            phone=None, date_birthday=None, gender=None):
        self.id = id
        self.user = user
        self.first_name = first_name
        self.date_join = date_join
        self.phone = phone
        self.date_birthday = date_birthday
        self.gender = gender

    __tablename__ = Table('profile', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    user = Column(unique=True)
    first_name = Column()
    date_join = Column(nullable=True)
    phone = Column(unique=True)
    date_birthday = Column(nullable=True)
    gender = Column()