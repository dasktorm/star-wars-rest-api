from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column (db.String(250), nullable=False)
    email = db.Column(db.String(90), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    favorites = db.relationship('Favorites',backref='people', lazy=True)

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    gender =  db.Column(db.String(250), nullable=False)
    hair_color =  db.Column(db.String(250), nullable=False)
    Favorites= db.relationship("favorites", backref="people", lazy=True)

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    orbital_period =  db.Column(db.String(250), nullable=False)
    population =  db.Column(db.String(250), nullable=False)
    Favorites = db.relationship("favorites", backref="planets", lazy=True)

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    def to_dict(self):
        return {}

class Favorite_Planets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    orbital_period =  db.Column(db.String(250), nullable=False)
    population =  db.Column(db.String(250), nullable=False)
    Favorites = db.relationship("favorites_planets", backref="favorite_planets", lazy=True)