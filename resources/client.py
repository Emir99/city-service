import os
import shutil

from flask import request, jsonify
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from db import db
from libs import image_helper
from models.client import ClientModel, ClientContactModel, ClientImageModel, ClientLanguageModel
from schemas.client import ClientSchema, ClientLanguageSchema, ClientContactSchema, ClientImageSchema

client_schema = ClientSchema(many=False)
clients_schema = ClientSchema(many=True, only=('identifier', 'forename', 'surname'))

client_language_schema = ClientLanguageSchema()
client_languages_schema = ClientLanguageSchema(many=True)

client_contact_schema = ClientContactSchema()
client_contacts_schema = ClientContactSchema(many=True)

client_images_schema = ClientImageSchema(many=True)


class ClientsResource(Resource):
    @classmethod
    def get(cls):
        all_clients = ClientModel.query.all()
        result = clients_schema.dump(all_clients)

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

            my_client = ClientModel(identifier, forename, surname, email, home_address, city, post_code, dob,
                                    residency, email_confirmation, role)
            db.session.add(my_client)

            query = db.session.query(ClientModel)
            client_id = str(query.filter_by(identifier=ClientModel.identifier)[-1]).split(" ")

            lang = request.json['languages']
            for i in range(len(lang)):
                name = request.json['languages'][i]['name']
                my_language = ClientLanguageModel(name, client_id[1][:-1])
                db.session.add(my_language)

            cont = request.json['contact_numbers']
            for i in range(len(cont)):
                number = request.json['contact_numbers'][i]['number']
                my_contact = ClientContactModel(number, client_id[1][:-1])
                db.session.add(my_contact)

            db.session.commit()

        if request.mimetype == 'multipart/form-data':

            data = {'images': None}
            try:
                query = db.session.query(ClientModel)
                cli_id = query.filter_by(identifier=ClientModel.identifier)[-1]
                identifier = client_schema.dump(cli_id)

                back_folder = "clients"
                client_id = f"{identifier['identifier']}".lower()
                folder = os.path.join(back_folder, client_id)
                for images in request.files.getlist('images'):
                    data['images'] = images
                    try:
                        save = image_helper.save_image(images, folder=folder)
                        # DATABASE
                        path = str(image_helper.get_path(save)).replace('\\', '/')
                        extension = image_helper.get_extension(save)
                        client_str = str(query.filter_by(identifier=ClientModel.identifier)[-1]).split(" ")
                        client_images = ClientImageModel(path, extension, client_str[1][:-1])
                        client_images.save_to_db()
                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data["images"])
                        return {"message": f"Extension {extension} not allowed!"}
            except IndexError:
                return {"message": "You need to create client first!"}

        return {'message': 'Client created successfully!'}, 200


class ClientResource(Resource):
    @classmethod
    def get(cls, identifier):
        client = ClientModel.find_by_identifier(identifier)
        if client:
            result = client_schema.dump(client)
            return jsonify(result)
        else:
            return {"message": f"Client with id {identifier} does not exist!"}

    @classmethod
    def put(cls, identifier):
        client = ClientModel.find_by_identifier(identifier)
        if client:
            if request.mimetype == 'application/json':
                client = ClientModel.find_by_identifier(identifier)

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

                client.forename = forename
                client.surname = surname
                client.email = email
                client.home_address = home_address
                client.city = city
                client.post_code = post_code
                client.dob = dob
                client.residency = residency
                client.email_confirmation = email_confirmation
                client.role = role

                db.session.commit()

                language = ClientLanguageModel.find_lang_by_client_id(identifier)
                if not language:
                    lang = request.json['languages']
                    for i in range(len(lang)):
                        name = request.json['languages'][i]['name']
                        my_language = ClientLanguageModel(name, identifier)
                        db.session.add(my_language)
                else:
                    for i in range(len(language)):
                        db.session.delete(language[i])
                        db.session.commit()
                    rang = request.json['languages']
                    for i in range(len(rang)):
                        name = request.json['languages'][i]['name']
                        my_language = ClientLanguageModel(name, identifier)
                        db.session.add(my_language)

                contact_number = ClientContactModel.find_cont_by_client_id(identifier)
                if not contact_number:
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ClientContactModel(number, identifier)
                        db.session.add(my_contact)
                else:
                    for i in range(len(contact_number)):
                        db.session.delete(contact_number[i])
                        db.session.commit()
                    cont = request.json['contact_numbers']
                    for i in range(len(cont)):
                        number = request.json['contact_numbers'][i]['number']
                        my_contact = ClientContactModel(number, identifier)
                        db.session.add(my_contact)

                db.session.commit()

            if request.mimetype == 'multipart/form-data':
                data = {'images': None}

                back_folder = "clients"
                client_id = f"{identifier}".lower()
                folder = os.path.join(back_folder, client_id)
                folder_path = os.path.join("static", "images", folder)
                is_folder = os.path.isdir(folder_path)
                if is_folder:
                    try:
                        shutil.rmtree(folder_path)
                    except OSError as e:
                        return jsonify("Error: %s : %s" % (folder_path, e.strerror))

                image_query = ClientImageModel.find_image_by_client_id(identifier)
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
                        client_image = ClientImageModel(path, extension, identifier)
                        client_image.save_to_db()

                    except UploadNotAllowed:
                        extension = image_helper.get_extension(data['images'])
                        return {"message": f"The file with {extension} is not allowed"}

            return {"message": f"Client updated successfully."}
        else:
            return {"message": f"Client with id {identifier} does not exist!"}

    @classmethod
    def delete(cls, identifier):
        client = ClientModel.find_by_identifier(identifier)
        if client:
            client.delete_from_db()
            back_folder = "clients"
            client_id = f"{identifier}".lower()
            folder = os.path.join(back_folder, client_id)
            folder_path = os.path.join("static", "images", folder)
            is_folder = os.path.isdir(folder_path)
            if is_folder:
                try:
                    shutil.rmtree(folder_path)
                except OSError as e:
                    return jsonify("Error: %s : %s" % (folder_path, e.strerror))

            return {'message': 'Client was deleted successfully!'}
        else:
            return {"message": f"Client {identifier} does not exist!"}
