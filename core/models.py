from sqlalchemy import create_engine, Integer
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session
from sqlalchemy.schema import Table, MetaData
from sqlalchemy_utils import EmailType

from settings import DB


class Main:

    def create_engine(self):
        return create_engine(
            "{}://{}:{}@{}/{}".format(
                DB["client"], DB["user"], DB["password"], DB["host"], DB["name_db"]
            ),
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


class CategoryItem(Base):

    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title

    __tablename__ = Table('category_item', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(unique=True)


class Location(Base):

    def __init__(self, id=None, article=None, title=None):
        self.id = id
        self.article = article
        self.title = title

    __tablename__ = Table('location', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(unique=True)
    article = Column()


class Item(Base):

    def __init__(self, id=None, category=None, article=None, attribute=None, title=None, location=None):
        self.id = id
        self.category = category
        self.article = article
        self.attribute = attribute
        self.title = title
        self.location = location

    __tablename__ = Table('item', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    article = Column()
    category = Column()
    location = Column()
    attribute = Column()
    title = Column()


class Food(Base):

    def __init__(self, id=None, item=None, user=None, amount=None, measure=None,
                 date_start=None, date_end=None, status=None):
        self.id = id
        self.item = item
        self.user = user
        self.date_start = date_start
        self.date_end = date_end
        self.status = status
        self.amount = amount
        self.measure = measure

    __tablename__ = Table('food', Main().create_metadata(), autoload=True)

    id = Column(Integer, primary_key=True, unique=True)
    item = Column(Integer, unique=True)
    user = Column(Integer, unique=True)
    date_start = Column()
    date_end = Column()
    status = Column()
    amount = Column()
    measure = Column()