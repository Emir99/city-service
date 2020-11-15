import os
import shutil

from flask import request, jsonify
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from db import db
from libs import image_helper
from models.category import CategoryModel
from models.subcategory import SubCategoryModel
from models.provider_req import ProviderModelReq, ProviderLanguageModelReq, ProviderContactModelReq,\
    ProviderImageModelReq
from schemas.provider_req import ProviderSchemaReq, ProviderLanguageSchemaReq, ProviderContactSchemaReq, \
    ProviderImageSchemaReq

from models.provider import ProviderModel, ProviderLanguageModel, ProviderContactModel, ProviderImageModel

provider_schema_req = ProviderSchemaReq(many=False)
providers_schema_req = ProviderSchemaReq(many=True, only=('identifier', 'forename', 'surname'))

provider_language_schema_req = ProviderLanguageSchemaReq()
providers_languages_schema_req = ProviderLanguageSchemaReq(many=True)

provider_contact_schema_req = ProviderContactSchemaReq()
provider_contacts_schema_req = ProviderContactSchemaReq(many=True)

provider_images_schema = ProviderImageSchemaReq(many=True)


class ProvidersReq(Resource):
    @classmethod
    def get(cls):
        all_provider_req = ProviderModelReq.query.all()
        result = providers_schema_req.dump(all_provider_req)

        return jsonify(result)

    @classmethod
    def post(cls):
        if request.mimetype == 'application/json':

            identifier = request.json['identifier']
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
            status = request.json['status']

            my_provider_req = ProviderModelReq(identifier, forename, surname, email, home_address, city, post_code, dob,
                                               residency, email_confirmation, role, status)
            db.session.add(my_provider_req)

            occupations = request.json['occupations']
            for i in range(len(occupations)):
                category_json = str(request.json['occupations'][i]['name'])
                category = CategoryModel.find_by_name(category_json)
                if category:
                    my_provider_req.occupations.append(category)
                    subcategories_len = request.json['occupations'][i]['subcategories']
                    for j in range(len(subcategories_len)):
                        subcategory_json = str(request.json['occupations'][i]['subcategories'][j]['name'])
                        category = str(CategoryModel.find_by_name(category_json)).split(" ")
                        sub = db.session.query(SubCategoryModel.name).\
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
                            my_provider_req.subcategories.append(subcategory_name)
                        else:
                            return {"message": f"Subcategory with name {subcategory_json} is not in {category_json}"}
                else:
                    return {"message": f"The category {category_json} does not exist!"}

            query = db.session.query(ProviderModelReq)
            provider_id = str(query.filter_by(identifier=ProviderModelReq.identifier)[-1]).split(" ")

            lang = request.json['languages']
            for i in range(len(lang)):
                name = request.json['languages'][i]['name']
                my_language = ProviderLanguageModelReq(name, provider_id[1][:-1])
                db.session.add(my_language)

            cont = request.json['contact_numbers']
            for i in range(len(cont)):
                number = request.json['contact_numbers'][i]['number']
                my_contact = ProviderContactModelReq(number, provider_id[1][:-1])
                db.session.add(my_contact)

            db.session.commit()

        if request.mimetype == 'multipart/form-data':

            data = {'images': None}
            try:
                query = db.session.query(ProviderModelReq)
                prov_req_id = query.filter_by(identifier=ProviderModelReq.identifier)[-1]
                identifier = provider_schema_req.dump(prov_req_id)

                back_folder = "providers"
                provider_id_req = f"{identifier['identifier']}".lower()
                folder = os.path.join(back_folder, provider_id_req)
                for images in request.files.getlist('images'):
                    data['images'] = images
                    try:
                        save = image_helper.save_image(images, folder=folder)
                        # DATABASE
                        path = str(image_helper.get_path(save)).replace('\\', '/')
                        extension = image_helper.get_extension(save)
                        provider_str = str(query.filter_by(identifier=ProviderModelReq.identifier)[-1]).split(" ")
                        provider_images = ProviderImageModelReq(path, extension, provider_str[1][:-1])
                        provider_images.save_to_db()
                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data["images"])
                        return {"message": f"Extension {extension} not allowed!"}
            except IndexError:
                return {"message": "You need to create provider first!"}

        return {'message': 'Provider request created successfully!'}, 200


class ProviderReq(Resource):
    @classmethod
    def get(cls, identifier):
        provider_req = ProviderModelReq.find_by_identifier(identifier)
        if provider_req:
            result = provider_schema_req.dump(provider_req)
            return jsonify(result)
        else:
            return {"message": f"Provider with id {identifier} does not exist!"}

    @classmethod
    def put(cls, identifier):
        provider_req = ProviderModelReq.find_by_identifier(identifier)
        if provider_req:
            if request.mimetype == 'application/json':
                provider_req = ProviderModelReq.find_by_identifier(identifier)

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
                status = request.json['status']

                provider_req.forename = forename
                provider_req.surname = surname
                provider_req.email = email
                provider_req.home_address = home_address
                provider_req.city = city
                provider_req.post_code = post_code
                provider_req.dob = dob
                provider_req.residency = residency
                provider_req.email_confirmation = email_confirmation
                provider_req.role = role
                provider_req.status = status

                db.session.commit()

                occupations_len = request.json['occupations']
                provider_req.occupations.clear()
                provider_req.subcategories.clear()

                for i in range(len(occupations_len)):
                    category_json = str(request.json['occupations'][i]['name'])
                    category = CategoryModel.find_by_name(category_json)
                    if category:
                        provider_req.occupations.append(category)
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
                                provider_req.subcategories.append(subcategory_name)
                            else:
                                return {"message":
                                        f"Subcategory with name {subcategory_json} is not in {category_json}!"}
                    else:
                        return {"message": f"Category {category_json} does not exist!"}

                language = ProviderLanguageModelReq.find_lang_by_provider_id(identifier)
                if not language:
                    lang = request.json['languages']
                    for i in range(len(lang)):
                        name = request.json['languages'][i]['name']
                        my_language = ProviderLanguageModelReq(name, identifier)
                        db.session.add(my_language)
                else:
                    for i in range(len(language)):
                        db.session.delete(language[i])
                        db.session.commit()
                    rang = request.json['languages']
                    for i in range(len(rang)):
                        name = request.json['languages'][i]['name']
                        my_language = ProviderLanguageModelReq(name, identifier)
                        db.session.add(my_language)

                contact_number = ProviderContactModelReq.find_cont_by_provider_id(identifier)
                if not contact_number:
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ProviderContactModelReq(number, identifier)
                        db.session.add(my_contact)
                else:
                    for i in range(len(contact_number)):
                        db.session.delete(contact_number[i])
                        db.session.commit()
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ProviderContactModelReq(number, identifier)
                        db.session.add(my_contact)

                db.session.commit()

                if status:
                    provider_id = identifier
                    my_provider = ProviderModel(identifier, forename, surname, email,
                                                home_address, city, post_code, dob,
                                                residency, email_confirmation, role)
                    db.session.add(my_provider)

                    provider = ProviderModel.find_by_identifier(identifier)

                    for i in range(len(occupations_len)):
                        category_json = str(request.json['occupations'][i]['name'])
                        category = CategoryModel.find_by_name(category_json)
                        provider.occupations.append(category)
                        subcategories_len = request.json['occupations'][i]['subcategories']
                        for j in range(len(subcategories_len)):
                            subcategory_json = str(request.json['occupations'][i]['subcategories'][j]['name'])
                            subcategory_name = SubCategoryModel.find_sub_by_name(subcategory_json)
                            provider.subcategories.append(subcategory_name)

                    rang = request.json['languages']
                    for i in range(len(rang)):
                        name = request.json['languages'][i]['name']
                        my_language = ProviderLanguageModel(name, provider_id)
                        db.session.add(my_language)

                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ProviderContactModel(number, provider_id)
                        db.session.add(my_contact)

                    images = ProviderImageModelReq.find_image_by_provider_id(provider_id)
                    result = provider_images_schema.dump(images)

                    for i in range(len(result)):
                        add = ProviderImageModel(result[i]['path'], result[i]['extension'], provider_id)
                        db.session.add(add)

                    provider_req.delete_from_db()

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

                image_query = ProviderImageModelReq.find_image_by_provider_id(identifier)
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
                        provider_image_req = ProviderImageModelReq(path, extension, identifier)
                        provider_image_req.save_to_db()

                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data['images'])
                        return {"message": f"The file with {extension} is not allowed"}

            return {'message': f'Provider Req updated!'}
        else:
            return {"message": f"Provider with id {identifier} does not exist!"}

    @classmethod
    def delete(cls, identifier):
        provider_req = ProviderModelReq.find_by_identifier(identifier)
        if provider_req:
            provider_req.delete_from_db()
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

            return {'message': 'Provider request was deleted successfully!'}
        else:
            return {"message": f"Provider {identifier} does not exist!"}
