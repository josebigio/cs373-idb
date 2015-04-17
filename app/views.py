from flask import render_template, json, make_response, jsonify, abort
from app import app, db, models
from .models import Element, Period, Group, Image, Trivia
from sqlalchemy import func
import subprocess


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
@app.route('/index')
def index():
    return render_template('Index.html')



@app.route('/api/<name>', methods=['GET'])
def api_handling(name):
    if name == 'element':
        return handle_element()
    elif name == 'period':
        return handle_period()
    elif name == 'group':
        return handle_group()
    elif name == 'trivia':
        return handle_trivia()
    else:
        return "Invalid API call"

@app.route('/api/period/<name>')
def handle_individual_period(name):    
    period_id = 0
    try:
        period_id = int(name)
    except:
        rabort(404)

    try:
        period = Period.query.get(period_id)
    except:
        abort(404)
    if period is None:
        abort(404)

    column_names = []
    for c in Period.__table__.columns:
        column_names.append(str(c).split("periods.")[1])
        
    result_dict = dict()
    for c_name in column_names:
        result_dict[c_name] = period.__dict__[c_name]

    return jsonify(result_dict)

@app.route('/api/group/<name>')
def handle_individual_group(name):    
    group_id = 0
    try:
        group_id = int(name)
    except:
        abort(404)
    try:
        group = Group.query.get(group_id)
    except:
        abort(404)
    if group is None:
        abort(404)

    column_names = []
    for c in Group.__table__.columns:
        column_names.append(str(c).split("groups.")[1])
        
    result_dict = dict()
    for c_name in column_names:
        result_dict[c_name] = group.__dict__[c_name]

    return jsonify(result_dict)


@app.route('/api/element/<atomic_number_str>')
def handle_individual_element(atomic_number_str):
    try:
        atomic_number = str(atomic_number_str)
    except:
        abort(404)
    element = Element.query.get(atomic_number)
    if element is None:
        abort(404)

    column_names = []
    for c in Element.__table__.columns:
        column_names.append(str(c).split("elements.")[1])
        
    result_dict = dict()
    for c_name in column_names:
        result_dict[c_name] = element.__dict__[c_name]


    return jsonify(result_dict)

@app.route('/api/trivia/<name>')
def handle_individual_trivia(name):    
    trivia_id = 0
    try:
        trivia_id = int(name)
    except:
        abort(404)

    trivia = Trivia.query.get(trivia_id)
    if trivia is None:
        abort(404)

    column_names = []
    for c in Trivia.__table__.columns:
        column_names.append(str(c).split("trivia.")[1])
        
    result_dict = dict()
    for c_name in column_names:
        result_dict[c_name] = trivia.__dict__[c_name]

    return jsonify(result_dict)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/timeline')
def timeline():
    elem_list = list(Element.query.all())
    result_list =[]
    for i in elem_list:
        result_list += [(i.year_of_discovery, i)]

    sorted(result_list, key=(lambda x: x[0]))

    #element_dict = [(1995, MockElement()), (1997, MockElement()), (2000, MockElement())]
    #return render_template('timeline.html')
    print(elem_list)
    return str(elem_list)

@app.route('/group/<name>')
def group(name=None):
    group_num = int(name)
    g = Group.query.get(group_num)
    elements = list(Element.query.filter_by(group_number=group_num).all())
    image_dict = {}
    for e in elements:
        image_dict[e] = Image.query.filter_by(element_number=e.atomic_number, image_type="default").first()
    return render_template('groupLayout.html', group=g, image_dict=image_dict)

@app.route('/element/<atomic_number_str>')
def element(atomic_number_str=None):
    atomic_number = int(atomic_number_str)
    e = Element.query.get(atomic_number)
    images = list(Image.query.filter_by(element_number=atomic_number).all())
    trivias = list(Trivia.query.filter_by(element_number=atomic_number).all())
    default_image = Image.query.filter_by(element_number=atomic_number, image_type="default").first()
    return render_template('elementLayout.html', element=e, images=images, default_image=default_image, trivias=trivias)

@app.route('/period/<name>')
def period(name=None):
    period_num = int(name)
    p = Period.query.get(period_num)
    elements = list(Element.query.filter_by(period_number=period_num).all())
    image_dict = {}
    for e in elements:
        image_dict[e] = Image.query.filter_by(element_number=e.atomic_number, image_type="default").first()
    return render_template('periodLayout.html', period=p, image_dict=image_dict)

@app.route('/tests/')
def run_tests_executor():
    return render_template("tests_executor.html")

@app.route('/testexecute/')
def run_tests():
    #os.system("./tests.py 2> output.txt")
    p = subprocess.Popen(['./tests.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    print(err)
    return render_template('tests.html', name=err)


#api handlers
def handle_element():
    elements = list(Element.query.all())
    result_dict = {}
    column_names = []
    for c in Element.__table__.columns:
        column_names.append(str(c).split("elements.")[1])    

    for element in elements:
        d = dict()
        for c_name in column_names:
            d[c_name] = element.__dict__[c_name]
        result_dict[element.atomic_number] = d
    
    return jsonify(result_dict)
        
def handle_period():
    periods = list(Period.query.all())
    result_dict = {}
    column_names = []
    for c in Period.__table__.columns:
        column_names.append(str(c).split("periods.")[1])

    for period in periods:
        d = dict()
        for c_name in column_names:
            d[c_name] = period.__dict__[c_name]
        result_dict[period.period_number] = d
 

    return jsonify(result_dict)

def handle_group():
    groups = list(Group.query.all())
    result_dict = {}
    column_names = []
    for c in Group.__table__.columns:
        column_names.append(str(c).split("groups.")[1])

    for group in groups:
        d = dict()
        for c_name in column_names:
            d[c_name] = group.__dict__[c_name]
        result_dict[group.group_number] = d
 

    return jsonify(result_dict)

def handle_trivia():
    trivias = list(Trivia.query.all())
    result_dict = {}
    column_names = []
    for c in Trivia.__table__.columns:
        column_names.append(str(c).split("trivia.")[1])

    for trivia in trivias:
        d = dict()
        for c_name in column_names:
            d[c_name] = trivia.__dict__[c_name]
        result_dict[trivia.id] = d
 

    return jsonify(result_dict)

