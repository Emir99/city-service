import os
from flask import Flask, request, send_file
from flask_uploads import configure_uploads, patch_request_class, UploadNotAllowed
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

from libs import image_helper
from resources.client import Client, Clients, ClientLanguage, ClientNumber, Avatar, avatar_schema
from libs.image_helper import IMAGE_SET
from db import db

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:emir1999@localhost/cityservice')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")
app.config['CORS_ENABLED'] = True

cors = CORS(app, resources={r"/client/*": {"origins": "*"}})

migrate = Migrate(app, db)
patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)

api.add_resource(Avatar, "/client/avatar/<string:uuid>")
api.add_resource(Clients, "/client")
api.add_resource(Client, "/client/<string:uuid>")
api.add_resource(ClientLanguage, "/client/language/<string:uuid>")
api.add_resource(ClientNumber, "/client/number/<string:uuid>")

db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
