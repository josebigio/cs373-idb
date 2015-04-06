"""
Object oriented representation of our data base structure. We will have 4 interweed entities: elements,
periods, groups and trivias
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

class Element(db.Model):
    """
    Represents an element on the period table. Eg: Hydrogen, Nitrogen, etc.
    """
    __tablename__ = 'elements'

    atomic_number = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(60))
    symbol = db.Column(db.String(3))
    period_number = db.Column(db.Integer)
    phase = db.Column(db.String(12))
    most_stable_crystal = db.Column(db.String(10))
    type = db.Column(db.String(30))
    ionic_radius = db.Column(db.Float)
    atomic_radius = db.Column(db.Float)
    electronegativity = db.Column(db.Float)
    first_ionization_potential = db.Column(db.Float)
    density = db.Column(db.Float)
    melting_point_k = db.Column(db.Float)
    boiling_point_k = db.Column(db.Float)
    isotopes = db.Column(db.Integer)
    discoverer = db.Column(db.String(50))
    year_of_discovery = db.Column(db.Integer)
    specific_heat_capacity = db.Column(db.Float)
    electron_configuration = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    group_number = db.Column(db.Integer, db.ForeignKey('groups.group_number'))


    # name = db.Column(db.String(50))
    # atomic_mass = db.Column(db.Float)
    # history = db.Column(db.Text)
    #group_column = db.Column(db.Integer, db.ForeignKey('group.column'))
    #period_row = db.Column(db.Integer, db.ForeignKey('period.row'))
    #trivias = db.relationship('Trivia',backref='element',lazy='dynamic')
    def __repr__(self):
        """
        Returns a string with information about the element such as atomic number, symbol, atomic mass, group and period
        """
        return '<Element %s. atomic_number = %d, symbol %s, group = %s, period = %d>' % (self.element, self.atomic_number,self.symbol,self.group_number,self.period_number)

class Period(db.Model):
    """
    Represents a period in the period table. A period can be though of the row number in the period table
    """
    __tablename__ = 'periods'

    period_number = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)

    def __repr__(self):
        """
        Returns a string with the row this period represents
        """
        return '<Period period_number: %d>' % self.period_number

class Group(db.Model):
    """
    Represents a group in the period table. For example alkali metals, alkaline metals, etc.
    """
    __tablename__ = 'groups'

    group_number = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    properties = db.Column(db.Text)
    applications = db.Column(db.Text)
    name = db.Column(db.Text)
    elements = db.relationship('Element',backref='group',lazy='dynamic')
    # trivias = db.relationship('Trivia',backref='group',lazy='dynamic')

    def __repr__(self):
        return '<Group name: %s>' % self.name

class Trivia(db.Model):
    """
    Represents a Trivia or cool snippet of information about an element, group or period. For example 
    did you know hydrogen is made in the sun?
    """

    __tablename__ = 'trivia'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    period_number = db.Column(db.Integer)
    group_number = db.Column(db.Integer)
    element_number = db.Column(db.Integer)

    #period_number = db.Column(db.Integer, db.ForeignKey('group.column'))
    #period_row = db.Column(db.Integer, db.ForeignKey('period.row'))
    #element_atomic_number = db.Column(db.Integer, db.ForeignKey('element.atomic_number'))
    
    def __repr__(self):
        return '<Trivia id: %d>' % self.trivia_id

class Image(db.Model):
    """
    Represents an image. They will be used through out the website, so they will have forein keys for 
    each of our 3 primary data tables (Elements, Groups and Periods)
    """

    __tablename__ = 'images'

    image_path = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)
    period_number = db.Column(db.Integer)
    group_number = db.Column(db.Integer)
    element_number = db.Column(db.Integer)