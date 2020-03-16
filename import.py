# import csv file of books into PostgreSQL database

import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
#

engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the
                                                    # database are kept separate

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    for isbn, title, author, year in reader: # loop gives each column a name
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                      {"isbn": isbn, "title": title, "author": author, "year": year}) # substitute values from CSV line into SQL command, as per this dict
        print(f"Added {title} by {author} with isbn {isbn}, written in {year}.")
    db.commit() # transactions are assumed, so close the transaction finished

if __name__ == "__main__":
    main()
