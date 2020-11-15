import os
import shutil

from flask import request, jsonify
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from db import db
from libs import image_helper

from models.category import CategoryModel, CategoryImageModel
from models.subcategory import SubCategoryModel
from schemas.category_subcategory import CategorySchema, SubCategorySchema, CategoryImageSchema

sub_category_schema = SubCategorySchema()
sub_categories_schema = SubCategorySchema(many=True, only=('name', 'description', 'icon_name'))

category_image_schema = CategoryImageSchema()

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=('name', 'description', 'icon_name'))


class Categories(Resource):
    @classmethod
    def get(cls):
        all_categories = CategoryModel.query.all()
        result = categories_schema.dump(all_categories)

        return jsonify(result)

    @classmethod
    def post(cls):
        if request.mimetype == 'application/json':
            category = request.get_json()
            name = category['name']
            description = category['description']
            icon_name = category['icon_name']

            my_category = CategoryModel(name, description, icon_name)
            db.session.add(my_category)
            """
            query = db.session.query(CategoryModel)
            category_id = str(query.filter_by(id=CategoryModel.id)[-1]).split(" ")
            
            sub_categories = category['subcategories']
            for i in range(len(sub_categories)):
                name = category['subcategories'][i]['name']
                description = category['subcategories'][i]['description']
                icon_name = category['subcategories'][i]['icon_name']
                my_sub = SubCategoryModel(name, description, icon_name, category_id[1][:-1])
                db.session.add(my_sub)
            """
            db.session.commit()

        if request.mimetype == 'multipart/form-data':
            data = {'images': None}
            query = db.session.query(CategoryModel)
            category_id = query.filter_by(id=CategoryModel.id)[-1]
            name = category_schema.dump(category_id)

            back_folder = "categories"
            category_name = f"{name['name']}".lower()
            folder = os.path.join(back_folder, category_name)
            for images in request.files.getlist('images'):
                data['images'] = images
                try:
                    save = image_helper.save_image(images, folder=folder)
                    # DATABASE
                    path = str(image_helper.get_path(save)).replace('\\', '/')
                    extension = image_helper.get_extension(save)
                    category_str = str(query.filter_by(id=CategoryModel.id)[-1]).split(" ")
                    category_image = CategoryImageModel(path, extension, category_str[1][:-1])
                    category_image.save_to_db()
                except UploadNotAllowed:
                    extension = image_helper.get_extension(data["images"])
                    return {"message": f"Extension {extension} not allowed!"}

        return {'message': 'Category uploaded successfully!'}


class Category(Resource):
    @classmethod
    def get(cls, name):
        category = CategoryModel.find_by_name(name)
        if category:
            query = db.session.query(CategoryModel)
            category_id = query.filter_by(name=name)[-1]
            result = category_schema.dump(category_id)
            return jsonify(result)
        else:
            return {"message": f"Category with name {name} does not exist!"}

    @classmethod
    def put(cls, name):
        category = CategoryModel.find_by_name(name)
        if category:
            if request.mimetype == 'application/json':
                category_json = request.get_json()
                name = category_json['name']
                description = category_json['description']
                icon_name = category_json['icon_name']

                category.name = name
                category.description = description
                category.icon_name = icon_name

                db.session.commit()
                """
                query = db.session.query(CategoryModel)
                category_id = query.filter_by(name=name)[-1]
                category_str = str(category_id).split(" ")
                query_sub = SubCategoryModel.find_sub_by_category_id(category_str[1][:-1])
                if not query_sub:
                    cont = category_json['subcategories']
                    for i in range(len(cont)):
                        name = category_json['subcategories'][i]['name']
                        description = category_json['subcategories'][i]['description']
                        icon_name = category_json['subcategories'][i]['icon_name']
                        my_sub = SubCategoryModel(name, description, icon_name, category_str[1][:-1])
                        db.session.add(my_sub)
    
                    db.session.commit()
                    return jsonify({'message': 'Category updated successfully.'})
    
                else:
                    for i in range(len(query_sub)):
                        db.session.delete(query_sub[i])
                        db.session.commit()
                    cont = category_json['subcategories']
                    for i in range(len(cont)):
                        name = category_json['subcategories'][i]['name']
                        description = category_json['subcategories'][i]['description']
                        icon_name = category_json['subcategories'][i]['icon_name']
                        my_sub = SubCategoryModel(name, description, icon_name, category_str[1][:-1])
                        db.session.add(my_sub)
                """
                db.session.commit()

            if request.mimetype == 'multipart/form-data':
                data = {'images': None}

                back_folder = "categories"
                category_name = f"{name}".lower()
                folder = os.path.join(back_folder, category_name)
                folder_path = os.path.join("static", "images", folder)
                is_folder = os.path.isdir(folder_path)
                if is_folder:
                    try:
                        shutil.rmtree(folder_path)
                    except OSError as e:
                        return jsonify("Error: %s : %s" % (folder_path, e.strerror))

                query = db.session.query(CategoryModel)
                category_id = query.filter_by(name=name)[-1]
                category_str = str(category_id).split(" ")
                image_query = CategoryImageModel.find_image_by_category_id(category_str[1][:-1])
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
                        category_id = query.filter_by(name=name)[-1]
                        category_str = str(category_id).split(" ")
                        category_image = CategoryImageModel(path, extension, category_str[1][:-1])
                        category_image.save_to_db()

                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data['images'])
                        return {"message": f"The file with {extension} is not allowed"}

            return {"message": "Category updated successfully!"}, 200
        else:
            return {"message": f"Category with name {name} does not exist!"}

    @classmethod
    def delete(cls, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category_id = str(CategoryModel.find_by_name(name)).split(" ")
            subcategories = SubCategoryModel.find_sub_by_category_id(category_id[1][:-1])
            result = sub_categories_schema.dump(subcategories)
            for i in range(len(result)):
                sub_name = result[i]['name'].lower()
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

            category.delete_from_db()

            back_folder = "categories"
            category_name = f"{name}".lower()
            folder = os.path.join(back_folder, category_name)
            folder_path = os.path.join("static", "images", folder)
            is_folder = os.path.isdir(folder_path)
            if is_folder:
                try:
                    shutil.rmtree(folder_path)
                except OSError as e:
                    return jsonify("Error: %s : %s" % (folder_path, e.strerror))

            return {'message': 'Category was deleted!'}

        else:
            return {"message": f"Category with name {name} does not exist!"}
