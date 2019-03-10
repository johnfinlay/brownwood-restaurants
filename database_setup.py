import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    phone = Column(String(12))
    website = Column(String(250))
    
    @property
    def serialize(self):
        return {
            'name'          : self.name,
            'address'       : self.address,
            'id'            : self.id,
            'phone'         : self.phone,
            'website'       : self.website,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name'          : self.name,
            'description'   : self.description,
            'id'            : self.id,
            'price'         : self.price,
            'course'        : self.course,
        }

class Message(Base):
    __tablename__ = 'messages'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    subject = Column(String(250))
    message = Column(String(1000))


engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)
