from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, create_engine, Date, Time, ForeignKey
from sqlalchemy_utils import create_database, database_exists

engine = create_engine("sqlite:///app.db?check_same_thread=False", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column("id",Integer,  primary_key=True)
    date = Column("date",String )
    time = Column("time", String, nullable=True)
    header = Column("header", String(80))
    description = Column("description", String(240), nullable=True)
    user = Column("user", Integer, ForeignKey("users.id"))

    def __init__(self, date, time, header,description, user ):
        super().__init__()
        self.date = date
        self.time = time
        self.header = header
        self.description = description
        self.user = user




class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    nickname = Column("nickname", String)
    email = Column("email", String)
    password = Column("password", String)
    def __init__(self, nickname, email, password):
        super().__init__()
        self.nickname = nickname
        self.email = email
        self.password = password

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)