from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    surname = Column (String(250), nullable=False)
    email = Column(String(90), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    favorites = relationship('Favorites',backref='people', lazy=True)

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    height = Column(String(250), nullable=False)
    gender =  Column(String(250), nullable=False)
    hair_color =  Column(String(250), nullable=False)
    Favorites= relationship("favorites", backref="people", lazy=True)

class Planets(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    diameter = Column(String(250), nullable=False)
    orbital_period =  Column(String(250), nullable=False)
    population =  Column(String(250), nullable=False)
    Favorites = relationship("favorites", backref="planets", lazy=True)

class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id =Column(Integer, ForeignKey('user.id'))
    planets_id = Column(Integer, ForeignKey('planets.id'))
    people_id = Column(Integer, ForeignKey('people.id'))
    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, '/models.py')