from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
import os
import sys

Base = declarative_base()


def delete_table():
    session.close()
    os.remove(".data/emails.db")
    sys.exit()


def create_database(eng):
    Base.metadata.create_all(eng)


class Mail(Base):
    __tablename__ = "Mails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)
    sender = Column(String)
    subject = Column(String)
    payload = Column(String)
    datetime = Column(String)
    to = Column(String)
    category = Column(String)


if __name__ == '__main__':
    engine = create_engine("sqlite:///.data/emails.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
