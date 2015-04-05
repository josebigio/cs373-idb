"""
Object oriented representation of our data base structure. We will have 4 interweed entities: elements,
periods, groups and trivias
"""

from app import db

class Element(db.Model):
    """
    Represents an element on the period table. Eg: Hydrogen, Nitrogen, etc.
    """
    __tablename__ = 'elements'

    atomic_number = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(60))
    symbol = db.Column(db.String(3))
    period_number = db.Column(db.Integer)
    group_number = db.Column(db.Integer)
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

# class Period(db.Model):
#     """
#     Represents a period in the period table. A period can be though of the row number in the period table
#     """
#     row = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.Text)
#     properties = db.Column(db.Text)
#     elements = db.relationship('Element',backref='period',lazy='dynamic')
#     trivias = db.relationship('Trivia',backref='period',lazy='dynamic')

#     def __init__(self, row, description="None", properties="None"):
#         self.row = row
#         self.description = description
#         self.properties = properties

#     def __repr__(self):
#         """
#         Returns a string with the row this period represents
#         """
#         return '<Period %s>' % self.row

# class Group(db.Model):
#     """
#     Represents a group in the period table. For example alkali metals, alkaline metals, etc.
#     """
#     column = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     information = db.Column(db.Text)
#     elements = db.relationship('Element',backref='group',lazy='dynamic')
#     trivias = db.relationship('Trivia',backref='group',lazy='dynamic')
    
#     def __init__(self, column,name, description="None", properties="None"):
#         self.column = column
#         self.name = name
#         self.description = description
#         self.properties = properties

#     def __repr__(self):
#         return '<Group %s>' % self.name

# class Trivia(db.Model):
#     """
#     Represents a Trivia or cool snippet of information about an element, group or period. For example 
#     did you know hydrogen is made in the sun?
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50))
#     description = db.Column(db.Text)
#     group_column = db.Column(db.Integer, db.ForeignKey('group.column'))
#     period_row = db.Column(db.Integer, db.ForeignKey('period.row'))
#     element_atomic_number = db.Column(db.Integer, db.ForeignKey('element.atomic_number'))
    
    
#     def __repr__(self):
#         return '<Group %s>' % self.name