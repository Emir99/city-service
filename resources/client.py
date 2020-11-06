import os
from flask import send_file, request, jsonify
from flask_restful import Resource
from flask_cors import cross_origin
from flask_uploads import UploadNotAllowed

from libs import image_helper
from db import db
from models.client import ClientModel, ClientLanguageModel, ClientContactModel
from schemas.client import ClientSchema, ClientLanguageSchema, ClientContactSchema
from schemas.avatar import AvatarSchema

avatar_schema = AvatarSchema()

language_schema = ClientContactSchema()
languages_schema = ClientLanguageSchema(many=True)

contact_schema = ClientContactSchema()
contacts_schema = ClientContactSchema(many=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


class Clients(Resource):
    @classmethod
    @cross_origin()
    def get(cls):
        all_clients = ClientModel.query.all()
        result = clients_schema.dump(all_clients)

        return jsonify(result)

    @classmethod
    @cross_origin()
    def post(cls):
        uuid = request.json['uuid']
        forename = request.json['forename']
        surname = request.json['surname']
        email = request.json['email']
        home_address = request.json['home_address']
        city = request.json['city']
        post_code = request.json['post_code']

        my_client = ClientModel(uuid, forename, surname, email, home_address, city, post_code)
        db.session.add(my_client)

        lang = request.json['languages']
        for i in range(len(lang)):
            name = request.json['languages'][i]['name']
            client_id = request.json['languages'][i]['client_id']
            my_language = ClientLanguageModel(name, client_id)
            db.session.add(my_language)

        cont = request.json['contact_numbers']
        for i in range(len(cont)):
            number = request.json['contact_numbers'][i]['number']
            client_id = request.json['contact_numbers'][i]['client_id']
            my_contact = ClientContactModel(number, client_id)
            db.session.add(my_contact)

        db.session.commit()

        return {'message': 'client created'}, 200


class Client(Resource):
    @classmethod
    @cross_origin()
    def get(cls, uuid):
        client = ClientModel.find_by_uuid(uuid)
        result = client_schema.dump(client)
        return jsonify(result)

    @classmethod
    @cross_origin()
    def put(cls, uuid):
        client = ClientModel.find_by_uuid(uuid)

        forename = request.json['forename']
        surname = request.json['surname']
        email = request.json['email']
        home_address = request.json['home_address']
        city = request.json['city']
        post_code = request.json['post_code']

        client.forename = forename
        client.surname = surname
        client.email = email
        client.home_address = home_address
        client.city = city
        client.post_code = post_code

        db.session.commit()

        language = ClientLanguageModel.find_lang_by_client_id(uuid)
        rang = request.json['languages']

        for i in range(len(rang)):
            lang = request.json['languages'][i]['name']
            language[i].name = lang
            db.session.commit()

        contact_number = ClientContactModel.find_num_by_client_id(uuid)
        leng = request.json['contact_numbers']

        for i in range(len(leng)):
            cont = request.json['contact_numbers'][i]['number']
            contact_number[i].number = cont
            db.session.commit()

        return jsonify({'message': 'Client updated!'})


class ClientLanguage(Resource):
    @classmethod
    @cross_origin()
    def post(cls, uuid):
        lang = request.get_json()
        for i in range(len(lang)):
            name = request.json[i]['name']
            my_language = ClientLanguageModel(name, uuid)
            db.session.add(my_language)

        db.session.commit()
        return jsonify({'message': 'Language is added'})


class ClientNumber(Resource):
    @classmethod
    @cross_origin()
    def post(cls, uuid):
        num = request.get_json()
        for i in range(len(num)):
            number = request.json[i]['number']
            my_number = ClientContactModel(number, uuid)
            db.session.add(my_number)

        db.session.commit()
        return jsonify({'message': 'Number is added'})


class Avatar(Resource):
    @classmethod
    @cross_origin()
    def get(cls, uuid):
        folder = "avatars"
        filename = f"user_{uuid}"
        avatar = image_helper.find_image_any_format(filename, folder)

        if avatar:
            return send_file(avatar)
        return {"message": "Avatar not found!"}, 404

    @classmethod
    @cross_origin()
    def put(cls, uuid):
        data = avatar_schema.load(request.files)
        filename = f"user_{uuid}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": "Deleting avatar failed!"}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": "Avatar uploaded."}
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": "This extension is not allowed!"}, 400
