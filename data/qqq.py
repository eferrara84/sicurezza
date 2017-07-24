from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.mail import Mail

if __name__ == '__main__':

    engine = create_engine("sqlite:///emails.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    mails = session.query(Mail).all()
    for m in mails:
        print m.payload