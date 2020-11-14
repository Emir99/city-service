from dotenv import load_dotenv
from flask import Flask
from flask_uploads import configure_uploads, patch_request_class
from flask_restful import Api
from flask_migrate import Migrate

from resources.client import ClientResource, ClientsResource
from resources.category import Category, Categories
from resources.subcategory import SubcategoriesCategory, Subcategories, Subcategory
from resources.provider_req import ProviderReq, ProvidersReq
from resources.provider import ProvidersResource, ProviderResource
from libs.image_helper import IMAGE_SET
from db import db

app = Flask(__name__)
api = Api(app)

load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

migrate = Migrate(app, db)
patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)

api.add_resource(ClientsResource, "/client")
api.add_resource(ClientResource, "/client/<string:identifier>")

api.add_resource(Categories, "/category")
api.add_resource(Category, "/category/<string:name>")

api.add_resource(SubcategoriesCategory, "/category/<string:category_name>/subcategory")
api.add_resource(Subcategories, "/category/subcategory")
api.add_resource(Subcategory, "/category/subcategory/<string:sub_name>")

api.add_resource(ProvidersReq, "/provider_req")
api.add_resource(ProviderReq, "/provider_req/<string:identifier>")

api.add_resource(ProvidersResource, "/provider")
api.add_resource(ProviderResource, "/provider/<string:identifier>")

db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
