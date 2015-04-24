#!flask/bin/python
import os
import unittest

from flask import json
from config import basedir
from app import app, db
from app.models import Element, Period, Group, Trivia

from app.views import perform_search
from app.views import getSnippet

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
        self.assertTrue(group.group_number == 1)
        self.assertTrue(group.description == "They are awesome")
        self.assertTrue(group.properties == "It has many properties")
        self.assertTrue(group.applications == "has bunch of applications")
        self.assertTrue(group.name == "Super name")

    def test_change_variables_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")
        group.applications = "They have different applications"
        db.session.add(group)
        db.session.commit()
        self.assertTrue(group.applications == "They have different applications")
    
    def test_create_period(self):
         period = Period(period_number=1,description="description")
         db.session.add(period)
         db.session.commit()
         self.assertTrue(period.period_number == 1)
         self.assertTrue(period.description == "description")


    def test_change_variables_period(self):
        period = Period(period_number=1,description="description")
        db.session.add(period)
        db.session.commit()

        period.description = "different"
        db.session.commit()
        self.assertTrue(period.description == "different")

    def test_create_element(self):  
        element = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description")
        db.session.add(element)
        db.session.commit()
        self.assertTrue(element.atomic_number == 1)
        self.assertTrue(element.symbol == 'H')
        self.assertTrue(element.element == "Hydrogen")
        self.assertTrue(element.phase == "phase")
        self.assertTrue(element.most_stable_crystal == "msc")
        self.assertTrue(element.type == "type")
        self.assertTrue(element.ionic_radius == 1.1)
        self.assertTrue(element.atomic_radius == 1.2)
        self.assertTrue(element.electronegativity == 2.0)
        self.assertTrue(element.first_ionization_potential == 3.0)
        self.assertTrue(element.density == 1.0)
        self.assertTrue(element.melting_point_k == 100.100)
        self.assertTrue(element.boiling_point_k == 100.100)
        self.assertTrue(element.isotopes == 4)
        self.assertTrue(element.discoverer == "Downing")
        self.assertTrue(element.year_of_discovery == 100)
        self.assertTrue(element.specific_heat_capacity == 100.100)
        self.assertTrue(element.electron_configuration == "electron_configuration")
        self.assertTrue(element.description == "description")


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
        self.assertTrue(elements == [element1,element2])  
    
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
        self.assertTrue(trivia.description == "Very hard trivia")

    
    def test_add_trivias_to_group(self):
        group = Group(group_number=1,description="They are awesome",properties="It has many properties", applications="has bunch of applications",name="Super name")
        db.session.add(group)
        db.session.commit()
        
        trivia1 = Trivia(description="Very hard trivia",group=group)
        db.session.add(trivia1)
        db.session.commit()

        trivia2 = Trivia(description="very hard trivia 2",group=group)
        db.session.add(trivia2)
        db.session.commit()

        trivias = group.trivias
        self.assertTrue(list(trivias)==[trivia1,trivia2])


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
        self.assertTrue(list(trivias)==[trivia1,trivia2])


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
        self.assertTrue(list(trivias)==[trivia1,trivia2])

    def test_api_element_1(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description")
            db.session.add(element)
            db.session.commit()
            resp = c.get('/api/element/1')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['element'], 'Hydrogen')
            self.assertEqual(data['atomic_number'], 1)
            self.assertEqual(data['symbol'], 'H')

    def test_api_element_2(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen")
            element2 = Element(atomic_number=2,symbol='He',element="Helium")
            element3 = Element(atomic_number=3,symbol='Li',element="Lithium")
            db.session.add(element)
            db.session.add(element2)
            db.session.add(element3)
            resp = c.get('/api/element/3')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['element'], 'Lithium')
            self.assertEqual(data['atomic_number'], 3)
            self.assertEqual(data['symbol'], 'Li')

    def test_api_element_3(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen")
            element2 = Element(atomic_number=2,symbol='He',element="Helium")
            element3 = Element(atomic_number=3,symbol='Li',element="Lithium")
            db.session.add(element)
            db.session.add(element2)
            db.session.add(element3)
            resp = c.get('/api/element/4')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '404 NOT FOUND')
            self.assertEqual(data, {'error': 'Not found'})

    def test_api_elements_4(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen",phase="phase",most_stable_crystal="msc",type="type",ionic_radius=1.1,atomic_radius=1.2,electronegativity=2.0,first_ionization_potential=3.0,density=1.0,melting_point_k=100.100,boiling_point_k=100.100,isotopes=4,discoverer="Downing",year_of_discovery=100,specific_heat_capacity=100.100,electron_configuration="electron_configuration",description="description")
            db.session.add(element)
            db.session.commit()
            resp = c.get('/api/element')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(len(data), 1)
            self.assertEqual(data['1']['symbol'], 'H')
            self.assertEqual(data['1']['element'], "Hydrogen")

    def test_api_elements_5(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen")
            element2 = Element(atomic_number=2,symbol='He',element="Helium")
            element3 = Element(atomic_number=3,symbol='Li',element="Lithium")
            db.session.add(element)
            db.session.add(element2)
            db.session.add(element3)
            db.session.commit()
            resp = c.get('/api/element')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(len(data), 3)
            self.assertEqual(data['1']['symbol'], 'H')
            self.assertEqual(data['1']['element'], "Hydrogen")
            self.assertEqual(data['2']['symbol'], 'He')
            self.assertEqual(data['2']['element'], "Helium")
            self.assertEqual(data['3']['symbol'], 'Li')
            self.assertEqual(data['3']['element'], "Lithium")

    def test_api_elements_6(self):
        with self.app as c:
            element = Element(atomic_number=1,symbol='H',element="Hydrogen")
            element2 = Element(atomic_number=2,symbol='He',element="Helium")
            element3 = Element(atomic_number=3,symbol='Li',element="Lithium")
            db.session.add(element)
            db.session.add(element2)
            db.session.add(element3)
            db.session.commit()
            resp = c.get('/api/element/')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '404 NOT FOUND')
            self.assertEqual(data, {'error': 'Not found'})

    ######Logan's Additions        
    def test_api_groups_1(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            db.session.add(group)
            db.session.commit()
            resp = c.get('/api/group')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(len(data), 1)
            self.assertEqual(data['1']['group_number'], 1)
            self.assertEqual(data['1']['name'], "Alkali")

    def test_api_groups_2(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            group2 = Group(group_number=2, name='Alkaline Earth', description="Common Salt Cation")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            db.session.add(group)
            db.session.add(group2)
            db.session.add(group3)
            db.session.commit()
            resp = c.get('/api/group')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 3)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['1']['group_number'], 1)
            self.assertEqual(data['1']['name'], "Alkali")
            self.assertEqual(data['2']['group_number'], 2)
            self.assertEqual(data['2']['name'], "Alkaline Earth")
            self.assertEqual(data['3']['group_number'], 3)
            self.assertEqual(data['3']['name'], "Halogens")

    def test_api_groups_3(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            group2 = Group(group_number=2, name='Alkaline Earth', description="Common Salt Cation")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            db.session.add(group)
            db.session.add(group2)
            db.session.add(group3)
            db.session.commit()
            resp = c.get('/api/group/')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '404 NOT FOUND')
            self.assertEqual(data, {'error': 'Not found'})

    def test_api_element_4(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            db.session.add(group)
            db.session.commit()
            resp = c.get('/api/group/1')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['group_number'], 1)
            self.assertEqual(data['name'], 'Alkali')
            self.assertEqual(data['description'], 'Explosions!')

    def test_api_groups_5(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            group2 = Group(group_number=2, name='Alkaline Earth', description="Common Salt Cation")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            db.session.add(group)
            db.session.add(group2)
            db.session.add(group3)
            db.session.commit()
            resp = c.get('/api/group/4')
            data = json.loads(resp.data)
            self.assertEqual(data, {'error': 'Not found'})

    def test_api_groups_6(self):
        with self.app as c:
            group = Group(group_number=1, name='Alkali', description="Explosions!")
            group2 = Group(group_number=2, name='Alkaline Earth', description="Common Salt Cation")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            db.session.add(group)
            db.session.add(group2)
            db.session.add(group3)
            db.session.commit()
            resp = c.get('/api/group')
            data = json.loads(resp.data)['3']
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['group_number'], 3)
            self.assertEqual(data['name'], 'Halogens')
            self.assertEqual(data['description'], 'Highly reactive, very poisonous')
            
    def test_api_period_1(self):
        with self.app as c:
            period = Period(period_number = 1, description = "The first period contains fewer elements than any other, with only two, hydrogen and helium")
            db.session.add(period)
            db.session.commit()
            resp = c.get('/api/period/1')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], "The first period contains fewer elements than any other, with only two, hydrogen and helium")

    def test_api_period_2(self):
        with self.app as c:
            period = Period(period_number = 2, description = "description of period 2")
            db.session.add(period)
            db.session.commit()
            resp = c.get('api/period/2')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], u"description of period 2")


    def test_api_period_3(self):
        with self.app as c:
            period = Period(period_number = 3, description = "description of period 3")
            db.session.add(period)
            db.session.commit()
            resp = c.get('api/period/3')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], u"description of period 3")

    def test_api_periods_1(self):
        with self.app as c:
            period1 = Period(period_number = 1, description = "description of period 1")
            period2 = Period(period_number = 2, description = "description of period 2")
            period3 = Period(period_number = 3, description = "description of period 3")
            period4 = Period(period_number = 4, description = "description of period 4")
            db.session.add(period1)
            db.session.add(period2)
            db.session.add(period3)
            db.session.add(period4)
            db.session.commit()
            resp = c.get('api/period')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(len(data), 4)

    def test_api_periods_2(self):
        with self.app as c:
            period1 = Period(period_number = 1, description = u"description of period 1")
            period2 = Period(period_number = 2, description = u"description of period 2")
            period3 = Period(period_number = 3, description = u"description of period 3")
            period4 = Period(period_number = 4, description = u"description of period 4")
            db.session.add(period1)
            db.session.add(period2)
            db.session.add(period3)
            db.session.add(period4)
            db.session.commit()
            resp = c.get('api/period/5')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '404 NOT FOUND')
            self.assertEqual(data, {'error': 'Not found'})


    def test_api_periods_3(self):
        with self.app as c:
            period1 = Period(period_number = 1, description = u"description of period 1")
            period2 = Period(period_number = 2, description = u"description of period 2")
            period3 = Period(period_number = 3, description = u"description of period 3")
            period4 = Period(period_number = 4, description = u"description of period 4")
            db.session.add(period1)
            db.session.add(period2)
            db.session.add(period3)
            db.session.add(period4)
            db.session.commit()
            resp = c.get('api/period')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['1']['description'], u"description of period 1")
            self.assertEqual(data['2']['description'], u"description of period 2")
            self.assertEqual(data['3']['description'], u"description of period 3")
            self.assertEqual(data['4']['description'], u"description of period 4")


    def test_api_trivia_1(self):
        with self.app as c:
            element = Element(atomic_number=2,symbol='e',element="Helioum")
            trivia = Trivia(description="description of trivia of element 2", element_number = 2, id = 1826)
            db.session.add(element)
            db.session.add(trivia)
            db.session.commit()
            resp = c.get('api/trivia/1826')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], u"description of trivia of element 2")
            self.assertEqual(data['element_number'], 2)

    def test_api_trivia_2(self):
        with self.app as c:
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            trivia = Trivia(description="description of trivia of group 3", group_number = 3, id = 1845)
            db.session.add(group3)
            db.session.add(trivia)
            db.session.commit()
            resp = c.get('api/trivia/1845')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], u"description of trivia of group 3")
            self.assertEqual(data['group_number'], 3)

    def test_api_trivia_3(self):
        with self.app as c:
            group4 = Group(group_number=4, name='Halogens', description="Highly reactive, very poisonous")
            trivia = Trivia(description="description of trivia of group 4", group_number = 4, id = 1826)
            db.session.add(group4)
            db.session.add(trivia)
            db.session.commit()
            resp = c.get('api/trivia/1826')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['description'], u"description of trivia of group 4")
            self.assertEqual(data['group_number'], 4)

    def test_api_trivias_1(self):
        with self.app as c:
            element = Element(atomic_number=2,symbol='e',element="Helioum")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            group4 = Group(group_number=4, name='Halogens', description="Highly reactive, very poisonous")
            trivia1 = Trivia(description="description of trivia of element 2", element_number = 2, id = 1826)
            trivia2 = Trivia(description="description of group 3", group_number = 3, id = 1845)
            trivia3 = Trivia(description="description of trivia of group 4", group_number = 4, id = 1836)
            db.session.add(element)
            db.session.add(group3)
            db.session.add(group4)
            db.session.add(trivia1)
            db.session.add(trivia2)
            db.session.add(trivia3)
            db.session.commit()
            resp = c.get('api/trivia')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(len(data), 3)


    def test_api_trivias_2(self):
        with self.app as c:
            element = Element(atomic_number=2,symbol='e',element="Helioum")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            group4 = Group(group_number=4, name='Halogens', description="Highly reactive, very poisonous")
            trivia1 = Trivia(description="description of trivia of element 2", element_number = 2, id = 1826)
            trivia2 = Trivia(description="description of group 3", group_number = 3, id = 1845)
            trivia3 = Trivia(description="description of trivia of group 4", group_number = 4, id = 1836)
            db.session.add(element)
            db.session.add(group3)
            db.session.add(group4)
            db.session.add(trivia1)
            db.session.add(trivia2)
            db.session.add(trivia3)
            db.session.commit()
            resp = c.get('api/trivia/18')
            data = json.loads(resp.data)
            self.assertEqual(data, {'error': 'Not found'})

    def test_api_trivias_3(self):
        with self.app as c:
            element = Element(atomic_number=2,symbol='e',element="Helioum")
            group3 = Group(group_number=3, name='Halogens', description="Highly reactive, very poisonous")
            group4 = Group(group_number=4, name='Halogens', description="Highly reactive, very poisonous")
            trivia1 = Trivia(description="description of trivia of element 2", element_number = 2, id = 1826)
            trivia2 = Trivia(description="description of trivia of group 3", group_number = 3, id = 1845)
            trivia3 = Trivia(description="description of trivia of group 4", group_number = 4, id = 1836)
            db.session.add(element)
            db.session.add(group3)
            db.session.add(group4)
            db.session.add(trivia1)
            db.session.add(trivia2)
            db.session.add(trivia3)
            db.session.commit()
            resp = c.get('api/trivia')
            data = json.loads(resp.data)
            self.assertEqual(resp.status, '200 OK')
            self.assertEqual(data['1826']['description'], u"description of trivia of element 2")
            self.assertEqual(data['1845']['description'], u"description of trivia of group 3")
            self.assertEqual(data['1836']['description'], u"description of trivia of group 4")

    def test_perform_search1(self):
        with self.app as c:
            element1 = Element(atomic_number=2, symbol='e', element='Hydrogen', phase = '13',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Colin',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1856, I think it is a good description',
                        column_number = 4,
                        group_number = 1,
                        period_number = 3)
            element2 = Element(atomic_number=3, symbol='r', element='Hydr', phase = '1r',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Meeee',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1886, I think it is a good description, do you think os too',
                        column_number = 3, group_number = 1, period_number = 3)
            period = Period(period_number = 3, description = "The first period contains fewer elements than any other, with only two, hydrogen and helium")
            db.session.add(period)
            group = Group(group_number=1, name='Halogens', description="Highly reactive, very poisonous", properties = "hey it is property", applications = "application is her etoo")
            db.session.add(group)
            db.session.add(element1)
            db.session.add(element2)
            db.session.commit()
            self.assertTrue(element1.element == 'Hydrogen')
            elements =list( Element.query.all())
            self.assertTrue(len(elements), 2)
            query = 'Hydr'
            result = perform_search(query)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], 3)
            self.assertEqual(result[0][1], 'r')


    def test_get_snippet(self):
        element1 = Element(atomic_number=2, symbol='e', element='Hydrogen', phase = '13',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Colin',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1856, I think it is a good description',
                        column_number = 4,
                        group_number = 1,
                        period_number = 3)
        element2 = Element(atomic_number=3, symbol='r', element='Hydr', phase = '1r',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Meeee',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1886, I think it is a good description, do you think os too',
                        column_number = 3, group_number = 1, period_number = 3)
        period = Period(period_number = 3, description = "The first period contains fewer elements than any other, with only two, hydrogen and helium")
        db.session.add(period)
        group = Group(group_number=1, name='Halogens', description="Highly reactive, very poisonous", properties = "hey it is property", applications = "application is her etoo")
        db.session.add(group)
        db.session.add(element1)
        db.session.add(element2)
        db.session.commit()
        query = 'Hydr'
        result = perform_search(query)
        result = result[0]
        snippet = getSnippet(result, query)
        self.assertEqual(snippet, u'It was discovered in 1886, I think it is a good description, do you think os to')


    def test_perform_search2(self):
        with self.app as c:
            element1 = Element(atomic_number=14, symbol='N', element='Nitrogen', phase = '13',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Colin',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1856, I think it is a good description',
                        column_number = 4,
                        group_number = 1,
                        period_number = 3)
            element2 = Element(atomic_number=10, symbol='r', element='Oxygen', phase = '1r',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Tehreem',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1886, I think it is a good description, do you think os too',
                        column_number = 3, group_number = 1, period_number = 3)
            period = Period(period_number = 3, description = "The first period contains fewer elements than any other, with only two, hydrogen and helium")
            db.session.add(period)
            group = Group(group_number=1, name='Halogens', description="Highly reactive, very poisonous", properties = "hey it is property", applications = "application is her etoo")
            db.session.add(group)
            db.session.add(element1)
            db.session.add(element2)
            db.session.commit()
            self.assertTrue(element1.element == 'Nitrogen')
            elements =list( Element.query.all())
            self.assertTrue(len(elements), 2)
            query = 'Nitrogen|13'
            result = perform_search(query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][3],'13')
            self.assertEqual(result[0][1], 'r')

#end of performsearch2
    def test_perform_search3(self):
        with self.app as c:
            element1 = Element(atomic_number=14, symbol='N', element='Nitrogen', phase = '13',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Colin',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1856, I think it is a good description',
                        column_number = 4,
                        group_number = 1,
                        period_number = 3)
            element2 = Element(atomic_number=10, symbol='O', element='Oxygen', phase = '1r',
                        most_stable_crystal = 'sth',
                        type = 'type',
                        ionic_radius = 1.2,
                        atomic_radius = 1.3,
                        electronegativity = 1.3,
                        first_ionization_potential = 1.3,
                        density = 1.2,
                        melting_point_k = 66.0,
                        boiling_point_k = 324.0,
                        isotopes = 3,
                        discoverer = 'Tehreem',
                        year_of_discovery = 1856,
                        specific_heat_capacity = 1.3,
                        electron_configuration = 'sth',
                        description = 'It was discovered in 1886, I think it is a good description, do you think os too',
                        column_number = 3, group_number = 1, period_number = 3)
            period = Period(period_number = 3, description = "The first period contains fewer elements than any other, with only two, hydrogen and helium")
            db.session.add(period)
            group = Group(group_number=1, name='Halogens', description="Highly reactive, very poisonous", properties = "hey it is property", applications = "application is her etoo")
            db.session.add(group)
            db.session.add(element1)
            db.session.add(element2)
            db.session.commit()
            self.assertTrue(element1.element == 'Nitrogen')
            self.assertTrue(element2.element == 'Oxygen')
            elements =list( Element.query.all())
            self.assertTrue(len(elements), 2)
            query = 'Oxygen&1856'
            result = perform_search(query)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0][0], 10)
            self.assertEqual(result[0][1], 'O')
            
def main():
    unittest.main()

if __name__ == '__main__':
    main()
