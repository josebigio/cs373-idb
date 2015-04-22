from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.images import Images

import os

app = Flask(__name__)
cwd = os.path.dirname(os.path.realpath(__file__))

image_paths = []
# Append all image folders to image path
for dir in os.listdir(cwd + '/static/images/'):
    if '.' not in dir:
        image_paths += 'static/images/' + dir
app.config['IMAGES_PATH'] = image_paths
app.config['IMAGES_CACHE'] = '/tmp/flask-images/'
app.secret_key = 'high_five'
images = Images(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models, views