'''
This code creates the mockup database for the Restaurant Catalog project by completing the tasks below;
- Creates the sqlite database and its tables/columns
- Maps python objects to those columns for CRUD operations
- Populates some data within those tables.

Comments galore; mostly to remind me the ORM concepts in Python and sqlalchemy for future reference.
Sqlalchemy components: Configuration, Class, Table. Mapper
'''

### Create the sqlite database and map python objects
## Configuration: import all modules needed
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Configuration: Create instance of declarative base (class code will inherit this)
Base = declarative_base()

##Class: Representation of table as a python class, extends the Base class
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Cuisine(Base):
    __tablename__ = 'cuisine'  # Table in the database

    # Mapper: Maps python objects to columns in the database
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    phone = Column(String(20))
    website = Column(String(30))
    address = Column(String(250))
    review = Column(String(3))  # would you eat here again? yes/no
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
    cuisine = relationship(Cuisine)  # Relationship to the actual class
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


#  JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'phone': self.phone,
            'website': self.website,
            'address': self.address,
        }

## Configuration: Create the database and tables
engine = create_engine('sqlite:///yycrestaurants.db')
Base.metadata.create_all(engine)

## Function to populate data
def populateData():
    ### Populate starter data in the database
    ## Bind the engine to the metadata of the Base class (enables declaratives to be accessed through a DBSession instance)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    # A DBSession() instance establishes all conversations with the database and represents a "staging zone"
    # for all the objects loaded into the database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call session.commit(). If you're not happy about the changes,
    # you can revert all of them back to the last commit by calling session.rollback()
    session = DBSession()

    ## Initial cuisines and restaurants. This code is a bit repetitive;
    # Trying to loop through list/dictionaries wasn't any shorter in terms of keeping the code DRY.
    #[ "Italian", "Indian", "Sushi", "Thai", "Vietnamese", "Burgers", "Canadian", "Asian", "Mexican"]

    cuisine1 = Cuisine(user_id=1,name="Italian")

    session.add(cuisine1)
    session.commit()

    italian1 = Restaurant(user_id=1,name="Teatro",
                          description=" Italian-influenced with hints of French. ",
                          phone="403-290-1012", website="http://www.teatro-rest.com/",
                          address="200 8th Ave SE Calgary, Alberta", cuisine=cuisine1)

    session.add(italian1)
    session.commit()

    italian2 = Restaurant(user_id=1,name="Posto",
                          description="Pizza and Italian small plates.",
                          phone="403-263-4876", website="http://www.posto.ca/",
                          address="1014 8 St. S.W. Calgary, Alberta", cuisine=cuisine1)

    session.add(italian2)
    session.commit()

    cuisine2 = Cuisine(user_id=1,name="Canadian")

    session.add(cuisine1)
    session.commit()

    canadian1 = Restaurant(user_id=1,name="Donna Mac",
                          description="Equal parts new-school sensitive and reliably classic.",
                          phone="403-719-3622", website="http://www.donnamacyyc.com/",
                          address="1002 9 St. S.W. Calgary, Alberta", cuisine=cuisine2)

    session.add(canadian1)
    session.commit()

    cuisine3 = Cuisine(user_id=1,name="Asian")

    session.add(cuisine3)
    session.commit()

    asian1 = Restaurant(user_id=1,name="Gorilla Whale",
                          description="Japanese gets funky in dishes that embrace high and low.",
                          phone="587-356-2686", website="http://www.donnamacyyc.com/",
                          address="1214 9 Ave. S.E. Calgary, Alberta", cuisine=cuisine3)

    session.add(asian1)
    session.commit()

    asian2 = Restaurant(user_id=1,name="Anju",
                          description="Contemporary Korean.",
                          phone="403-460-3341", website="http://www.anju.ca/",
                          address="105, 344 17 Ave. S.W. Calgary, Alberta", cuisine=cuisine3)

    session.add(asian2)
    session.commit()

    cuisine4 = Cuisine(user_id=1,name="Mexican")

    session.add(cuisine4)
    session.commit()

    mexican1 = Restaurant(user_id=1,name="Anejo",
                          description="Handcrafted recipes cooked to perfection in Mexican style "
                                      "with a flair for contemporary flavours",
                          phone="587-353-2656", website="http://www.anejo.ca/",
                          address="2116 4 St. S.W. Calgary, Alberta", cuisine=cuisine4)

    session.add(mexican1)
    session.commit()

## If the script is directly executed, populate data in tables
if __name__ == '__main__':
    populateData()