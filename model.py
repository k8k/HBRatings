from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime
from sqlalchemy import ForeignKey


ENGINE = None
Session = None
ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, 
                                    autocommit = False,
                                    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key = True)
    email       = Column(String(64), nullable=True, unique=True)
    password    = Column(String(64), nullable=True)
    age         = Column(Integer, nullable=True)
    gender      = Column(String(1), nullable=True)
    occupation  = Column(String(40), nullable=True)
    zipcode     = Column(String(15), nullable=True)

    def __str__(self):
        output = "ID: %r, EMAIL: %s, PASSWORD: %r,\n" % (self.id, self.email, 
            self.password)
        output += "AGE: %r, GENDER: %s, OCCUPATION: %s,\n" % (self.age, self.gender, 
            self.occupation)
        output += "ZIPCODE: %s" % self.zipcode
        return output


class Movie (Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable=False)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(120), nullable=True)

    def __str__(self):
        new_date = datetime.strftime(self.released_at, "%d-%b-%Y")
        output = "ID: %r, TITLE: %s,\n" % (self.id, self.name)
        output += "RELEASED: %r, URL: %s" % (new_date, self.imdb_url)
        return output

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key= True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer(1), nullable = False)

    movie = relationship("Movie",
        backref = backref("ratings", order_by=id))

    user = relationship("User",
        backref = backref("ratings",order_by = id))

    def __str__(self):
        output = "ID: %r, MOVIE ID: %r,\n" % (self.id, self.movie_id)
        output += "USER ID: %r, RATING: %r" % (self.user_id, self.rating)
        return output



### End class declarations

# def connect():
#     global ENGINE
#     global Session



#     return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
