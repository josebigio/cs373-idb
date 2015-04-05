from flask import render_template
from app import app, db, models
import subprocess

@app.route('/')
@app.route('/index')
def index():
    return render_template('Index.html')


@app.route('/models/<name>')
def models(name=1):
    e = models.Element.query.get(int(name))
    return e

@app.route('/about')
def about():
    return render_template('Groups.html')


@app.route('/group/<name>')
def group(name=None):
    if name == 'alkali':
        return render_template('alkaliLayout.html', name=name)
    elif name == 'alkaline-earth':
        return render_template('alkalinearthLayout.html', name=name)
    elif name == 'halogen':
        return render_template('halogenLayout.html', name=name)
    else:
        return "Page not found!"


@app.route('/element/<name>')
def element(name=None):
    if name == 'helium':
        return render_template('Helium.html', name=name)
    elif name == 'hydrogen':
        return render_template('Hydrogen.html', name=name)
    elif name == 'fluorine':
        return render_template('Fluorine.html', name=name)
    else:
        return "Page not found!"


@app.route('/period/<name>')
def period(name=None):
    if name == '1':
        return render_template('periodOneLayout.html', name=name)
    elif name == '2':
        return render_template('periodTwoLayout.html', name=name)
    elif name == '3':
        return render_template('periodThreeLayout.html', name=name)
    else:
        return "Page not found!"


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

