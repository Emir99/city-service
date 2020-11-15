import os
import shutil

from flask import request, jsonify
from flask_cors import cross_origin
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from db import db
from libs import image_helper
from models.category import CategoryModel
from models.subcategory import SubCategoryModel
from models.provider import ProviderModel, ProviderLanguageModel, ProviderContactModel, ProviderImageModel
from schemas.provider import ProviderSchema, ProviderLanguageSchema, ProviderContactSchema, ProviderImageSchema

provider_schema = ProviderSchema(many=False)
providers_schema = ProviderSchema(many=True, only=('identifier', 'forename', 'surname'))

provider_language_schema = ProviderLanguageSchema()
providers_languages_schema = ProviderLanguageSchema(many=True)

provider_contact_schema = ProviderContactSchema()
provider_contacts_schema = ProviderContactSchema(many=True)

provider_images_schema = ProviderImageSchema(many=True)


class ProvidersResource(Resource):
    @classmethod
    @cross_origin
    def get(cls):
        all_providers = ProviderModel.query.all()
        result = providers_schema.dump(all_providers)

        return jsonify(result)


class ProviderResource(Resource):
    @classmethod
    @cross_origin
    def get(cls, identifier):
        provider = ProviderModel.find_by_identifier(identifier)
        if provider:
            result = provider_schema.dump(provider)
            return jsonify(result)
        else:
            return {"message": f"Provider with id {identifier} does not exist!"}

    @classmethod
    @cross_origin
    def put(cls, identifier):
        provider = ProviderModel.find_by_identifier(identifier)
        if provider:
            if request.mimetype == 'application/json':
                provider = ProviderModel.find_by_identifier(identifier)

                forename = request.json['forename']
                surname = request.json['surname']
                email = request.json['email']
                home_address = request.json['home_address']
                city = request.json['city']
                post_code = request.json['post_code']
                dob = request.json['dob']
                residency = request.json['residency']
                email_confirmation = request.json['email_confirmation']
                role = request.json['role']

                provider.forename = forename
                provider.surname = surname
                provider.email = email
                provider.home_address = home_address
                provider.city = city
                provider.post_code = post_code
                provider.dob = dob
                provider.residency = residency
                provider.email_confirmation = email_confirmation
                provider.role = role

                db.session.commit()

                occupations_len = request.json['occupations']
                provider.occupations.clear()
                provider.subcategories.clear()

                for i in range(len(occupations_len)):
                    category_json = str(request.json['occupations'][i]['name'])
                    category = CategoryModel.find_by_name(category_json)
                    if category:
                        provider.occupations.append(category)
                        subcategories_len = request.json['occupations'][i]['subcategories']
                        for j in range(len(subcategories_len)):
                            subcategory_json = str(request.json['occupations'][i]['subcategories'][j]['name'])
                            category = str(CategoryModel.find_by_name(category_json)).split(" ")
                            sub = db.session.query(SubCategoryModel.name). \
                                filter(SubCategoryModel.category_id == category[1][:-1]).all()
                            sub_len = len(sub) - 1

                            def is_sub(length, sub_name):
                                try:
                                    fix = sub.pop(length)
                                    if sub_name in fix[0]:
                                        return True
                                    else:
                                        return is_sub(length - 1, sub_name)
                                except IndexError:
                                    return False

                            check_sub = is_sub(sub_len, subcategory_json)
                            if check_sub:
                                subcategory_name = SubCategoryModel.find_sub_by_name(subcategory_json)
                                provider.subcategories.append(subcategory_name)
                            else:
                                return {"message":
                                        f"Subcategory with name {subcategory_json} is not in {category_json}!"}
                    else:
                        return {"message": f"Category {category_json} does not exist!"}

                language = ProviderLanguageModel.find_lang_by_provider_id(identifier)
                if not language:
                    lang = request.json['languages']
                    for i in range(len(lang)):
                        name = request.json['languages'][i]['name']
                        my_language = ProviderLanguageModel(name, identifier)
                        db.session.add(my_language)
                else:
                    for i in range(len(language)):
                        db.session.delete(language[i])
                        db.session.commit()
                    rang = request.json['languages']
                    for i in range(len(rang)):
                        name = request.json['languages'][i]['name']
                        my_language = ProviderLanguageModel(name, identifier)
                        db.session.add(my_language)

                contact_number = ProviderContactModel.find_cont_by_provider_id(identifier)
                if not contact_number:
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ProviderContactModel(number, identifier)
                        db.session.add(my_contact)
                else:
                    for i in range(len(contact_number)):
                        db.session.delete(contact_number[i])
                        db.session.commit()
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ProviderContactModel(number, identifier)
                        db.session.add(my_contact)

                db.session.commit()

            if request.mimetype == 'multipart/form-data':
                data = {'images': None}

                back_folder = "providers"
                provider_id = f"{identifier}".lower()
                folder = os.path.join(back_folder, provider_id)
                folder_path = os.path.join("static", "images", folder)
                is_folder = os.path.isdir(folder_path)
                if is_folder:
                    try:
                        shutil.rmtree(folder_path)
                    except OSError as e:
                        return jsonify("Error: %s : %s" % (folder_path, e.strerror))

                image_query = ProviderImageModel.find_image_by_provider_id(identifier)
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
                        provider_image = ProviderImageModel(path, extension, identifier)
                        provider_image.save_to_db()

                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data['images'])
                        return {"message": f"The file with {extension} is not allowed"}

            return {"message": f"Provider updated successfully."}
        else:
            return {"message": f"Provider with id {identifier} does not exist!"}

    @classmethod
    @cross_origin
    def delete(cls, identifier):
        provider = ProviderModel.find_by_identifier(identifier)
        if provider:
            provider.delete_from_db()
            back_folder = "providers"
            provider_id = f"{identifier}".lower()
            folder = os.path.join(back_folder, provider_id)
            folder_path = os.path.join("static", "images", folder)
            is_folder = os.path.isdir(folder_path)
            if is_folder:
                try:
                    shutil.rmtree(folder_path)
                except OSError as e:
                    return jsonify("Error: %s : %s" % (folder_path, e.strerror))

            return {'message': 'Provider was deleted successfully!'}
        else:
            return {"message": f"Provider {identifier} does not exist!"}
