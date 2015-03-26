#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import Element, Period, Group, Trivia

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_group(self):
        group = Group(1,"Alkali","They are awesome","It has many properties")
        db.session.add(group)
        db.session.commit()
        assert(group.column == 1)
        assert(group.description == "They are awesome")
        assert(group.properties == "It has many properties")

    def test_change_variables_group(self):
        group = Group(1,"Alkali","They are awesome","It has many properties")
        group.information = "They have many informations"
        db.session.add(group)
        db.session.commit()
        assert(group.information == "They have many informations")
        
    def test_create_period(self):
        period = Period(1,"They are awesome","It has many properties")
        db.session.add(period)
        db.session.commit()
        assert(period.row == 1)
        assert(period.description == "They are awesome")
        assert(period.properties == "It has many properties")

    def test_change_variables_period(self):
        period = Period(1,"They are awesome","It has many properties")
        period.row = 2
        db.session.add(period)
        db.session.commit()
        assert(period.row == 2)

    def test_change_variables_period(self):
        period = Period(1,"They are awesome","It has many properties")
        period.row = 2
        db.session.add(period)
        db.session.commit()
        assert(period.row == 2)

    def test_create_element(self):        
        element = Element(atomic_number=1,symbol='H',name="Hydrogen",atomic_mass=1.001,history="it is forged in the sun")
        db.session.add(element)
        db.session.commit()
        assert(element.atomic_number == 1)
        assert(element.symbol == 'H')
        assert(element.name == "Hydrogen")
        assert(element.atomic_mass == 1.001)
        assert(element.history == "it is forged in the sun")

    def test_add_elements_to_period(self):
        period = Period(1,"They are awesome","It has many properties")
        db.session.add(period)
        db.session.commit()

        element1 = Element(atomic_number=1,symbol='H',name="Hydrogen",atomic_mass=1.001,history="it is forged in the sun",period=period)
        db.session.add(element1)
        db.session.commit()

        element2 = Element(atomic_number=2,symbol='He',name="Helium",atomic_mass=4.002,history="it makes balloons fly",period=period)
        db.session.add(element2)
        db.session.commit()

        elements = list(period.elements)
        assert elements == [element1,element2]

    def test_add_elements_to_group(self):
        group = Group(1,"Alkali","They are awesome","It has many properties")
        db.session.add(group)
        db.session.commit()

        element1 = Element(atomic_number=3,symbol='Li',name="Lithium",atomic_mass=6.94,history="w/e",group=group)
        db.session.add(element1)
        db.session.commit()

        element2 = Element(atomic_number=11,symbol='Na',name="Sodium",atomic_mass=22.989,history="its salty",group=group)
        db.session.add(element2)
        db.session.commit()

        elements = list(group.elements)
        assert elements == [element1,element2]


    def test_create_trivia(self):   
        trivia = Trivia(title="Super Hard",description="Very hard trivia")
        db.session.add(trivia)
        db.session.commit()
        assert(trivia.title == "Super Hard")
        assert(trivia.description == "Very hard trivia")
    
    def test_add_trivias_to_group(self):   
        group = Group(1,"Alkali","They are awesome","It has many properties")
        db.session.add(group)
        db.session.commit()

        trivia1 = Trivia(title="Super Hard",description="Very hard trivia",group=group)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(title="Super Easy",description="Very easy trivia",group=group)
        db.session.add(trivia2)
        db.session.commit()

        trivias = list(group.trivias)
        assert trivias == [trivia1,trivia2]

    def test_add_trivias_to_period(self):   
        period = Period(1,"They are awesome","It has many properties")
        db.session.add(period)
        db.session.commit()

        trivia1 = Trivia(title="Super Hard",description="Very hard trivia",period=period)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(title="Super Easy",description="Very easy trivia",period=period)
        db.session.add(trivia2)
        db.session.commit()

        trivias = list(period.trivias)
        assert trivias == [trivia1,trivia2]

    def test_add_trivias_to_element(self):   
        element = Element(atomic_number=3,symbol='Li',name="Lithium",atomic_mass=6.94,history="w/e")
        db.session.add(element)
        db.session.commit()

        trivia1 = Trivia(title="Super Hard",description="Very hard trivia",element=element)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(title="Super Easy",description="Very easy trivia",element=element)
        db.session.add(trivia2)
        db.session.commit()

        trivias = list(element.trivias)
        assert trivias == [trivia1,trivia2]


if __name__ == '__main__':
    unittest.main()