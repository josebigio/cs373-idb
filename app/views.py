from flask import render_template, json, make_response, jsonify, abort, request
from app import app, db, models
from .models import Element, Period, Group, Image, Trivia, MockElement
from sqlalchemy import func

import urllib2
import subprocess
import re


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
@app.route('/index')
def index():
    return render_template('Index.html')



@app.route('/api/<name>', methods=['GET'])
def api_handling(name):
    columns = request.args.get('columns')
    column_set = set()
    if columns is not None:
        column_set = set(columns.split(','))
    if name == 'element':
        return handle_element(column_set)
    elif name == 'period':
        return handle_period(column_set)
    elif name == 'group':
        return handle_group(column_set)
    elif name == 'trivia':
        return handle_trivia(column_set)
    else:
        return "Invalid API call"

@app.route('/api/period/<name>', methods=['GET'])
def handle_individual_period(name):
    period_id = 0
    columns = request.args.get('columns')
    column_set = set()
    if columns is not None:
        column_set = set(columns.split(','))
    try:
        period_id = int(name)
    except:
        abort(404)

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
        if columns is None or c_name in column_set:
            result_dict[c_name] = period.__dict__[c_name]

    return jsonify(result_dict)

@app.route('/api/group/<name>', methods=['GET'])
def handle_individual_group(name):
    group_id = 0
    columns = request.args.get('columns')
    column_set = set()
    if columns is not None:
        column_set = set(columns.split(','))
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
        if columns is None or c_name in column_set:
            result_dict[c_name] = group.__dict__[c_name]

    return jsonify(result_dict)


@app.route('/api/element/<atomic_number_str>', methods=['GET'])
def handle_individual_element(atomic_number_str):
    columns = request.args.get('columns')
    column_set = set()
    if columns is not None:
        column_set = set(columns.split(','))
    try:
        atomic_number = str(atomic_number_str)
    except:
        abort(404)
        return
    element = Element.query.get(atomic_number)
    if element is None:
        abort(404)
        return
    column_names = []
    for c in Element.__table__.columns:
        column_names.append(str(c).split("elements.")[1])

    result_dict = dict()
    for c_name in column_names:
        if columns is None or c_name in column_set:
            result_dict[c_name] = element.__dict__[c_name]

    return jsonify(result_dict)


@app.route('/api/trivia/<name>', methods=['GET'])
def handle_individual_trivia(name):
    trivia_id = 0
    columns = request.args.get('columns')
    column_set = set()
    if columns is not None:
        column_set = set(columns.split(','))
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
        if columns is None or c_name in column_set:
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
        if not (i.year_of_discovery == None or i.discoverer == None):
            image_default = Image.query.filter_by(element_number = i.atomic_number, image_type ="default").first()
            result_list += [(i.year_of_discovery, i, image_default)]

    result_list.sort(key= lambda x : x[0])

    return render_template('timeline.html', elements = result_list)

@app.route('/charts')
def charts():
    elem_list = list(Element.query.all())
    elem_dict = {}
    for e in elem_list:
        if(e.atomic_number!=None and e.element!=None and e.melting_point!=None and e.boiling_point!=None):
            elem_dict[e.atomic_number] = (e.element, e.melting_point, e.boiling_point)

    return render_template('charts.html', elem_dict = elem_dict)

def getLatLonFromMapUrl(map_url):
    lat = 0
    lon = 0
    lat_pattern = re.compile(r'2d(.+?)!', flags=re.DOTALL)
    lon_pattern = re.compile(r'3d(.+?)!', flags=re.DOTALL)
    try:
        lon = float(lat_pattern.findall(map_url)[0])
        lat = float(lon_pattern.findall(map_url)[0])
    except ValueError as e:
        print("Error processing lat, lon: " + str(e))
    return lat, lon


@app.route('/funRun')
def funRunApi():

    response = urllib2.urlopen('http://104.239.139.43:8000/api/funruns')
    data = json.load(response)
    fun_run_arr = data.get('funruns')
    result = []
    for fun_run in fun_run_arr:
        lat, lon = getLatLonFromMapUrl(fun_run['map_url'])
        result.append([lat, lon, fun_run['name'].encode('ascii','ignore'), fun_run['website'].encode('ascii','ignore')])
    return render_template("funRunApi.html", funRunArr=result)

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


@app.route('/search')
def search():
    columns = request.args.get('columns')
    query = request.args.get('q').strip('+')
    results=[{'url':'/element/2', 'snippet':['Paramapagaga', 'He', 'jahajh'], 'title':'Helium'}, {'url':'/element/3', 'snippet':['Paramapagaga', 'He', 'jahajh'], 'title':'Paraaa'}]
    return render_template('search.html', query=query, results=results, size=len(results))


#api handlers
def handle_element(column_set):
    elements = list(Element.query.all())
    result_dict = {}
    column_names = []
    for c in Element.__table__.columns:
        column_names.append(str(c).split("elements.")[1])

    for element in elements:
        d = dict()
        for c_name in column_names:
            if len(column_set) == 0 or c_name in column_set:
                d[c_name] = element.__dict__[c_name]
        result_dict[element.atomic_number] = d

    return jsonify(result_dict)

def handle_element_project(column_set):
    elements = list(Element.query.all())
    result_dict = {}
    column_names = []
    for c in Element.__table__.columns:
        column_names.append(str(c).split("elements.")[1])

    for element in elements:
        d = dict()
        for c_name in column_names:
            if len(column_set) == 0 or c_name in column_set:
                d[c_name] = element.__dict__[c_name]
        result_dict[element.atomic_number] = d

    return jsonify(result_dict)

def handle_period(column_set):
    periods = list(Period.query.all())
    result_dict = {}
    column_names = []
    for c in Period.__table__.columns:
        column_names.append(str(c).split("periods.")[1])

    for period in periods:
        d = dict()
        for c_name in column_names:
            if len(column_set) == 0 or c_name in column_set:
                d[c_name] = period.__dict__[c_name]
        result_dict[period.period_number] = d


    return jsonify(result_dict)

def handle_group(column_set):
    groups = list(Group.query.all())
    result_dict = {}
    column_names = []
    for c in Group.__table__.columns:
        column_names.append(str(c).split("groups.")[1])

    for group in groups:
        d = dict()
        for c_name in column_names:
            if len(column_set) == 0 or c_name in column_set:
                d[c_name] = group.__dict__[c_name]
        result_dict[group.group_number] = d


    return jsonify(result_dict)

def handle_trivia(column_set):
    trivias = list(Trivia.query.all())
    result_dict = {}
    column_names = []
    for c in Trivia.__table__.columns:
        column_names.append(str(c).split("trivia.")[1])

    for trivia in trivias:
        d = dict()
        for c_name in column_names:
            if len(column_set) == 0 or c_name in column_set:
                d[c_name] = trivia.__dict__[c_name]
        result_dict[trivia.id] = d

    return jsonify(result_dict)

