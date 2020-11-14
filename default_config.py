import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:emir1999@localhost/cityservice'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADED_IMAGES_DEST = os.path.join("static", "images")