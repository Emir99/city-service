import os
import shutil

from flask import request, jsonify
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from db import db
from libs import image_helper

from models.category import CategoryModel
from models.subcategory import SubCategoryModel, SubCategoryImageModel
from schemas.category_subcategory import CategorySchema, SubCategorySchema, CategoryImageSchema

sub_category_schema = SubCategorySchema()
sub_categories_schema = SubCategorySchema(many=True, only=('name', 'description', 'icon_name'))

category_image_schema = CategoryImageSchema()

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=('name', 'description', 'icon_name'))


class SubcategoriesCategory(Resource):
    @classmethod
    def get(cls, category_name):
        category_id = str(CategoryModel.find_by_name(category_name)).split(" ")

        if category_id[0] == 'None':
            return {"message": "Category does not exist!"}
        else:
            subcategories = SubCategoryModel.find_sub_by_category_id(category_id[1][:-1])
            result = sub_categories_schema.dump(subcategories)
            return jsonify(result)

    @classmethod
    def post(cls, category_name):
        category_id = str(CategoryModel.find_by_name(category_name)).split(" ")

        if category_id[0] == 'None':
            return {"message": "Category does not exist!"}
        else:
            if request.mimetype == 'application/json':
                subcategory = request.get_json()
                name = subcategory['name']
                description = subcategory['description']
                icon_name = subcategory['icon_name']

                query = db.session.query(CategoryModel)
                category_id = query.filter_by(name=category_name)[-1]
                category_str = str(category_id).split(" ")

                my_category = SubCategoryModel(name, description, icon_name, category_str[1][:-1])
                db.session.add(my_category)
                db.session.commit()

            if request.mimetype == 'multipart/form-data':
                data = {'images': None}
                query = db.session.query(SubCategoryModel)
                subcategory_id = query.filter_by(id=SubCategoryModel.id)[-1]
                name = category_schema.dump(subcategory_id)

                back_folder = "subcategories"
                subcategory_name = f"{name['name']}".lower()
                folder = os.path.join(back_folder, subcategory_name)
                for images in request.files.getlist('images'):
                    data['images'] = images
                    try:
                        save = image_helper.save_image(images, folder=folder)
                        # DATABASE
                        path = str(image_helper.get_path(save)).replace('\\', '/')
                        extension = image_helper.get_extension(save)
                        subcategory_str = str(query.filter_by(id=SubCategoryModel.id)[-1]).split(" ")
                        subcategory_image = SubCategoryImageModel(path, extension, subcategory_str[1][:-1])
                        subcategory_image.save_to_db()
                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data["images"])
                        return jsonify({"message": f"Extension {extension} not allowed!"})

            return {"message": "Subcategory created successfully."}, 200


class Subcategories(Resource):
    @classmethod
    def get(cls):
        all_categories = SubCategoryModel.query.all()
        result = sub_categories_schema.dump(all_categories)

        return jsonify(result)


class Subcategory(Resource):
    @classmethod
    def get(cls, sub_name):
        subcategory = SubCategoryModel.find_sub_by_name(sub_name)

        if subcategory:
            query = db.session.query(SubCategoryModel)
            subcategory_id = query.filter_by(name=sub_name)[-1]
            result = sub_category_schema.dump(subcategory_id)
            return jsonify(result)
        else:
            return {"message": f"Subcategory with name {sub_name} does not exist!"}

    @classmethod
    def put(cls, sub_name):
        subcategory = SubCategoryModel.find_sub_by_name(sub_name)

        if subcategory:
            if request.mimetype == 'application/json':
                subcategory = SubCategoryModel.find_sub_by_name(sub_name)
                subcategory_json = request.get_json()
                name = subcategory_json['name']
                description = subcategory_json['description']
                icon_name = subcategory_json['icon_name']

                subcategory.name = name
                subcategory.description = description
                subcategory.icon_name = icon_name

                db.session.commit()

            if request.mimetype == 'multipart/form-data':
                data = {'images': None}

                back_folder = "subcategories"
                subcategory_name = f"{sub_name}".lower()
                folder = os.path.join(back_folder, subcategory_name)
                folder_path = os.path.join("static", "images", folder)
                is_folder = os.path.isdir(folder_path)
                if is_folder:
                    try:
                        shutil.rmtree(folder_path)
                    except OSError as e:
                        return jsonify("Error: %s : %s" % (folder_path, e.strerror))

                query = db.session.query(SubCategoryModel)
                subcategory_id = query.filter_by(name=sub_name)[-1]
                subcategory_str = str(subcategory_id).split(" ")
                image_query = SubCategoryImageModel.find_image_by_subcategory_id(subcategory_str[1][:-1])
                for i in range(len(image_query)):
                    db.session.delete(image_query[i])
                    db.session.commit()

                for images in request.files.getlist('images'):
                    data['images'] = images
                    try:
                        save = image_helper.save_image(images, folder=folder, name=images.filename)
                        # DATABASE
                        path = str(image_helper.get_path(save)).replace('\\', '/')
                        extension = image_helper.get_extension(save)
                        subcategory_id = query.filter_by(name=sub_name)[-1]
                        subcategory_str = str(subcategory_id).split(" ")
                        category_image = SubCategoryImageModel(path, extension, subcategory_str[1][:-1])
                        category_image.save_to_db()

                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data['images'])
                        return {"message": f"The file with {extension} is not allowed"}

            return {"message": "Subcategory updated successfully."}, 200

        else:
            return {"message": f"Subcategory with name {sub_name} does not exist!"}

    @classmethod
    def delete(cls, sub_name):
        subcategory = SubCategoryModel.find_sub_by_name(sub_name)
        if subcategory:
            subcategory.delete_from_db()

            back_folder = "subcategories"
            subcategory_name = f"{sub_name}".lower()
            folder = os.path.join(back_folder, subcategory_name)
            folder_path = os.path.join("static", "images", folder)
            is_folder = os.path.isdir(folder_path)
            if is_folder:
                try:
                    shutil.rmtree(folder_path)
                except OSError as e:
                    return jsonify("Error: %s : %s" % (folder_path, e.strerror))

            return {'message': 'Subcategory was deleted!'}

        else:
            return {"message": f"Subcategory with name {sub_name} does not exist!"}
