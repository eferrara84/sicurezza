from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv

from model.mail import Mail

if __name__ == '__main__':

    engine = create_engine("sqlite:///emails.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # write to csv file all payloads
    mails = session.query(Mail).all()
    with open('ems.csv', 'wb') as csvfile:
        for m in mails:
            spamwriter = csv.writer(csvfile, delimiter=' ')
            spamwriter.writerow([m.payload])
