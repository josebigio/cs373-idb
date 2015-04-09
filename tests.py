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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testing_db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")
        db.session.add(group)
        db.session.commit()
        assert(group.group_number == 1)
        assert(group.description == "They are awesome")
        assert(group.properties == "It has many properties")
        assert(group.applications == "has bunch of applications")
        assert(group.name == "Super name")

    def test_change_variables_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")
        group.applications = "They have different applications"
        db.session.add(group)
        db.session.commit()
        assert(group.applications == "They have different applications")
    
    def test_create_period(self):
         period = Period(period_number=1,description="description")
         db.session.add(period)
         db.session.commit()
         assert(period.period_number == 1)
         assert(period.description == "description")


    def test_change_variables_period(self):
        period = Period(period_number=1,description="description")
        db.session.add(period)
        db.session.commit()

        period.description = "different"
        db.session.commit()
        assert(period.description == "different")

    def test_create_element(self):  
        element = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description")
        db.session.add(element)
        db.session.commit()
        assert(element.atomic_number == 1)
        assert(element.symbol == 'H')
        assert(element.element == "Hydrogen")
        assert(element.phase == "phase")
        assert(element.most_stable_crystal == "msc")
        assert(element.type == "type")
        assert(element.ionic_radius == 1.1)
        assert(element.atomic_radius == 1.2)
        assert(element.electronegativity == 2.0)
        assert(element.first_ionization_potential == 3.0)
        assert(element.density == 1.0)
        assert(element.melting_point_k == 100.100)
        assert(element.boiling_point_k == 100.100)
        assert(element.isotopes == 4)
        assert(element.discoverer == "Downing")
        assert(element.year_of_discovery == 100)
        assert(element.specific_heat_capacity == 100.100)
        assert(element.electron_configuration == "electron_configuration")
        assert(element.description == "description")


    def test_add_elements_to_period(self):
        
        period = Period(period_number=1,description="description")
        db.session.add(period)
        db.session.commit()    
    
        element1 = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description",period=period)
        db.session.add(element1)
        db.session.commit()
 
        element2 = Element(atomic_number=2,symbol='He',element="Helium",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description",period=period)

        db.session.add(element2)
        db.session.commit()

        elements = list(period.elements) 
        assert(elements == [element1,element2])  
    
    def test_add_elements_to_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")

        db.session.add(group)
        db.session.commit()

        element1 = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description",group=group)
        db.session.add(element1)
        db.session.commit()

        element2 = Element(atomic_number=2,symbol='He',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description",group=group)
        db.session.add(element2)
        db.session.commit()

        elements = list(group.elements)
        assert elements == [element1,element2]

    
    def test_create_trivia(self):   
        trivia = Trivia(description="Very hard trivia")
        db.session.add(trivia)
        db.session.commit()
        assert(trivia.description == "Very hard trivia")
<<<<<<< HEAD
    
    def test_add_trivias_to_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")
        db.session.add(group)
        db.session.commit()
        
        trivia1 = Trivia(description="Very hard trivia",group=group)
        db.session.add(trivia1)
        db.session.commit()
=======


    # def test_add_trivias_to_group(self):
    #     group = Group(1,"Alkali","They are awesome","It has many properties")
    #     db.session.add(group)
    #     db.session.commit()
>>>>>>> de6d5fc08219649301220661a1727644425a626b

        trivia2 = Trivia(description="very hard trivia 2",group=group)
        db.session.add(trivia2)
        db.session.commit()

        trivias = group.trivias
        assert (list(trivias)==[trivia1,trivia2])


    def test_add_trivias_to_period(self):
        period = Period(period_number=1,description="They are awesome")
        db.session.add(period)
        db.session.commit()
        
        trivia1 = Trivia(description="Very hard trivia",period=period)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(description="very hard trivia 2",period=period)
        db.session.add(trivia2)
        db.session.commit()

        trivias = period.trivias
        assert (list(trivias)==[trivia1,trivia2])


    def test_add_trivias_to_element(self):
        element = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description")
        db.session.add(element)
        db.session.commit()       
 
        trivia1 = Trivia(description="Very hard trivia",element=element)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(description="very hard trivia 2",element=element)
        db.session.add(trivia2)
        db.session.commit()

        trivias = element.trivias
        assert (list(trivias)==[trivia1,trivia2])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
