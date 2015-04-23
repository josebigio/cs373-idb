from flask import render_template, json, make_response, jsonify, abort, request
from app import app, db, models
from .models import Element, Period, Group, Image, Trivia, MockElement
from sqlalchemy import func
from flask.ext.images import Images, resized_img_src

import urllib2
import subprocess
import re

standard_image_width = 500
standard_image_height = 500


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


@app.route('/FunWithChemistry')
def FunWithChemistry():
    return render_template('FunWithChemistry.html')


def getFileFromPath(filePath):
    return filePath.split('/')[-1]

@app.route('/timeline')
def timeline():
    elem_list = list(Element.query.all())
    result_list = []
    for i in elem_list:
        if not (i.year_of_discovery == None or i.discoverer == None):
            image_default = Image.query.filter_by(element_number = i.atomic_number, image_type ="default").first()
            image_default.image_path = resized_img_src(getFileFromPath(image_default.image_path),
                                                 width=standard_image_width, height=standard_image_height)
            result_list += [(i.year_of_discovery, i, image_default)]

    result_list.sort(key= lambda x : x[0])

    return render_template('timeline.html', elements=result_list, test=app.config['IMAGES_PATH'])

@app.route('/charts')
def charts():
    elem_list = list(Element.query.all())
    elem_dict = {}
    for e in elem_list:
        if(e.atomic_number!=None and e.element!=None and e.melting_point_k!=None and e.boiling_point_k!=None):
            elem_dict[e.atomic_number] = (e.element, e.melting_point_k, e.boiling_point_k)

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
        image_default = Image.query.filter_by(element_number=e.atomic_number, image_type="default").first()
        image_default.image_path = resized_img_src(getFileFromPath(image_default.image_path),
                                                 width=standard_image_width, height=standard_image_height)
        image_dict[e] = image_default
    return render_template('groupLayout.html', group=g, image_dict=image_dict)

@app.route('/element/<atomic_number_str>')
def element(atomic_number_str=None):
    atomic_number = int(atomic_number_str)
    e = Element.query.get(atomic_number)
    images = list(Image.query.filter_by(element_number=atomic_number).all())
    for i in images:
        if i.image_type != "default":
            i.image_path = resized_img_src(getFileFromPath(i.image_path),
                                                 width=standard_image_width, height=standard_image_height)

    trivias = list(Trivia.query.filter_by(element_number=atomic_number).all())
    image_default = Image.query.filter_by(element_number=atomic_number, image_type="default").first()
    return render_template('elementLayout.html', element=e, images=images, default_image=image_default, trivias=trivias)

@app.route('/period/<name>')
def period(name=None):
    period_num = int(name)
    p = Period.query.get(period_num)
    elements = list(Element.query.filter_by(period_number=period_num).all())
    image_dict = {}
    for e in elements:
        image_default = Image.query.filter_by(element_number=e.atomic_number, image_type="default").first()
        image_default.image_path = resized_img_src(getFileFromPath(image_default.image_path),
                                                 width=standard_image_width, height=standard_image_height)
        image_dict[e] = image_default
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
    query = request.args.get('q').lower().strip().split(' ')
    q = request.args.get('q').strip()
    if(len(query) > 1):
        q1 = q.replace(' ', '&')
        q2 = q.replace(' ', '|')
        search_result1 = perform_search(q1)
        search_result2 = perform_search(q2)
        res1 = to_list(search_result1, query)
        res2 = to_list(search_result2, query)
        #res3 = to_list_period(search_result1, query)
        #res4 = to_list_period(search_result2, query)
        results = res1 + res2# + res3 + res4
    else:
        results = perform_search(q)
        result1 = to_list(results, query)
        #result2 = to_list_period(results, query)
        results = result1# + result2
    return render_template('search.html', query=query, title_query = ' '.join(query), results=results, size=len(results))

#helper method to return list from search_result
def to_list(search_result, query):
    results = []
    pattern = re.compile('[^A-Za-z0-9/-]+')
    for row in search_result:
        d = {}
        d['url'] = '/element/' + str(row[0])
        d['title'] = row[2]
        snippet = getSnippet(row, query)
        d['snippet'] = list(zip(snippet.split(), pattern.sub(' ', snippet.lower()).split()))
        results.append(d)
    return results

'''
#helper method to return list from search_result
def to_list_period(search_result, query):
    results = []
    pattern = re.compile('[^A-Za-z0-9/-]+')
    for row in search_result:
        d = {}
        d['url'] = '/period/' + str(row[4])
        d['title'] = 'Period ' + str(row[4])
        snippet = getSnippetPeriod(row, query)
        d['snippet'] = list(zip(snippet.split(), pattern.sub(' ', snippet.lower()).split()))
        results.append(d)
    return results'''

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



#search query result
def perform_search(query):
    statement = """SELECT atomic_number, symbol, element, period_number, column_number, phase, most_stable_crystal, type, ionic_radius, electronegativity, first_ionization_potential, density, melting_point_k,
 boiling_point_k, isotopes, year_of_discovery, specific_heat_capacity, electron_configuration, discoverer, description FROM (SELECT atomic_number, symbol, element, period_number, column_number, phase, most_stable_crystal, type, ionic_radius, electronegativity, first_ionization_potential, density, melting_point_k,
 boiling_point_k, isotopes, year_of_discovery, specific_heat_capacity, electron_configuration, discoverer, description, 
	setweight(to_tsvector(CAST(atomic_number AS VARCHAR)),'A') ||
			  setweight(to_tsvector(element), 'A' )||
	  setweight(to_tsvector('simple', symbol), 'A')||
    setweight(to_tsvector(CAST(period_number AS VARCHAR)), 'D') ||
    setweight(to_tsvector(CAST(column_number AS VARCHAR)), 'D') ||
              setweight(to_tsvector(coalesce(string_agg(CAST(phase AS VARCHAR), ' '),'')), 'C') ||
    setweight(to_tsvector('simple',coalesce(string_agg(CAST(most_stable_crystal AS VARCHAR), ' '), '')),'C') ||
    			 setweight(to_tsvector('simple',coalesce(string_agg(CAST(type AS VARCHAR), ' '), '')), 'C') ||
     setweight(to_tsvector('simple',coalesce(string_agg(CAST(ionic_radius AS VARCHAR), ' '), '')), 'D') ||
    setweight(to_tsvector('simple',coalesce(string_agg(CAST(atomic_radius AS VARCHAR), ' '), '')), 'C') ||
setweight(to_tsvector('simple',coalesce(string_agg(CAST(electronegativity AS VARCHAR), ' '), '')), 'C') ||
setweight(to_tsvector('simple',coalesce(string_agg(CAST(first_ionization_potential AS VARCHAR), ' '), '')), 'C') ||
		  setweight(to_tsvector(coalesce(string_agg(CAST(density AS VARCHAR), ' '), '')), 'C') ||
  setweight(to_tsvector('simple', coalesce(string_agg(CAST(melting_point_k AS VARCHAR), ' '), '')), 'C') ||
  setweight(to_tsvector('simple', coalesce(string_agg(CAST(boiling_point_k AS VARCHAR), ' '), '')), 'C') ||
        setweight(to_tsvector('simple', coalesce(string_agg(CAST(isotopes AS VARCHAR), ' '), '')), 'C') ||
         setweight(to_tsvector('simple', coalesce(string_agg(CAST(year_of_discovery AS VARCHAR), ' '), '')), 'B') ||
setweight(to_tsvector('simple', coalesce(string_agg(CAST(specific_heat_capacity AS VARCHAR), ' '), '')), 'B') ||
setweight(to_tsvector('simple',coalesce(string_agg(CAST(electron_configuration AS VARCHAR), ' '), '')), 'C') ||
setweight(to_tsvector('simple', coalesce(string_agg(discoverer, ' '), '')), 'A') ||
setweight(to_tsvector(description), 'B')
	as document from elements
  group by atomic_number) p
	WHERE p.document @@ to_tsquery('{!s}')
	ORDER BY ts_rank(p.document, to_tsquery('{!s}')) DESC;""".format(query, query)


    result = db.engine.execute(statement).fetchall()
    return result


#get snippet of the description of an element
def getSnippet(result, query):
    number = result[0]
    element = Element.query.get(number)
    desc = element.description.lower()
    match_indices = []
    for q in query:
        match = desc.find(q.lower())
        if(match != -1):
            match_indices.append(match)
    if (len(match_indices) == 0):
        return element.description[:70]
    min_index = min(match_indices)
    max_index = max(match_indices)
    left_index = min_index
    right_index = max_index
    if (min_index < 70):
         left_index = 0
    else:
        left_index = left_index - 70
    if (max_index > len(desc)-70):
        right_index = len(desc)-1
    else:
        right_index = right_index + 70 
    desc = element.description
    description = desc[left_index:right_index]
    return description


'''
def getSnippetPeriod(result, query):
    period_num= result[4]
    period = Period.query.get(period_num)
    desc = period.description.lower()
    match_indices = []
    for q in query:
        match = desc.find(q.lower())
        if(match != -1):
            match_indices.append(match)
    if (len(match_indices) == 0):
        return period.description[:(len(match_indices)-10)]
    min_index = min(match_indices)
    max_index = max(match_indices)
    left_index = min_index
    right_index = max_index
    if (min_index < 20):
         left_index = 0
    else:
        left_index = left_index - 20
    if (max_index > len(desc)-20):
        right_index = len(desc)-1
    else:
        right_index = right_index + 20
    desc = period.description
    description = desc[left_index:right_index]
    return description'''
