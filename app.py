import os
import traceback

from myproject import app, db
from flask import jsonify, request, send_file
from flask_cors import CORS, cross_origin
from myproject.clientmodels import ClientModel, LanguageModel, ContactModel
from myproject.clientschemas import ClientSchema, LanguageSchema, ContactSchema

from flask_uploads import UploadNotAllowed, configure_uploads, patch_request_class
from myproject import image_helper
from myproject.imageschema import ImageSchema
from myproject.image_helper import IMAGE_SET

app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")

CORS(app)

image_schema = ImageSchema()
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)

language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@app.route('/client', methods=['POST'])
@cross_origin()
def add_client():
    uuid = request.json['uuid']
    forename = request.json['forename']
    surname = request.json['surname']
    email = request.json['email']
    homeAddress = request.json['homeAddress']
    city = request.json['city']
    postCode = request.json['postCode']

    my_client = ClientModel(uuid, forename, surname, email, homeAddress, city, postCode)
    db.session.add(my_client)

    lang = request.json['languages']
    for i in range(len(lang)):
        name = request.json['languages'][i]['name']
        client_id = request.json['languages'][i]['client_id']
        my_language = LanguageModel(name, client_id)
        db.session.add(my_language)

    cont = request.json['contact_numbers']
    for i in range(len(cont)):
        number = request.json['contact_numbers'][i]['number']
        client_id = request.json['contact_numbers'][i]['client_id']
        my_contact = ContactModel(number, client_id)
        db.session.add(my_contact)

    db.session.commit()
    
    return {'message': 'client created'}, 200

@app.route('/client', methods=['GET'] )
@cross_origin()
def get_all_clients():
    all_clients = ClientModel.query.all()
    result = clients_schema.dump(all_clients)

    return jsonify(result)  

@app.route('/client/<string:uuid>', methods=['GET'])
@cross_origin()
def getclient_by_uuid(uuid):
    client = ClientModel.find_by_uuid(uuid)
    result = client_schema.dump(client)
    return jsonify(result)

@app.route('/client/<string:uuid>', methods=['PUT'])
@cross_origin()
def client_update(uuid):
    client = ClientModel.find_by_uuid(uuid)
    
    forename = request.json['forename']
    surname = request.json['surname']
    email = request.json['email']
    homeAddress = request.json['homeAddress']
    city = request.json['city']
    postCode = request.json['postCode']

    client.forename = forename
    client.surname = surname
    client.email = email
    client.homeAddress = homeAddress
    client.city = city
    client.postCode = postCode

    db.session.commit()

    language = LanguageModel.findlang_by_client_id(uuid)
    rang = request.json['languages']

    for i in range(len(rang)):
        lang = request.json['languages'][i]['name']
        language[i].name = lang
        db.session.commit()

    contact_number = ContactModel.findcont_by_client_id(uuid)
    leng = request.json['contact_numbers']

    for i in range(len(leng)):
        cont = request.json['contact_numbers'][i]['number']
        contact_number[i].number = cont
        db.session.commit()

    return jsonify({'message': 'Client updated!'})

@app.route('/client/<string:uuid>', methods=['DELETE'])
@cross_origin()
def delete_client(uuid):
    client = ClientModel.find_by_uuid(uuid)
    delete = ClientModel.delete_from_db(client)

    return jsonify({'message': 'client deleted'})

@app.route('/client/language/<string:uuid>', methods=['POST'])
@cross_origin()
def add_lang(uuid):
    lang = request.get_json()
    for i in range(len(lang)):
        name = request.json[i]['name']
        my_language = LanguageModel(name, uuid)
        db.session.add(my_language)

    db.session.commit()
    return jsonify({'message': 'Language is added'})

@app.route('/client/number/<string:uuid>', methods=['POST'])
@cross_origin()
def add_num(uuid):
    num = request.get_json()
    for i in range(len(num)):
        number = request.json[i]['number']
        my_number = ContactModel(number, uuid)
        db.session.add(my_number)

    db.session.commit()
    return jsonify({'message': 'Number is added'})

@app.route('/client/<string:uuid>/image', methods=['POST'])
@cross_origin()
def add_image(uuid):
    data = image_schema.load(request.files)
    folder = f"user_{uuid}"
    try:
        image_path = image_helper.save_image(data["image"], folder=folder)
        basename = image_helper.get_basename(image_path)
        return {"message": "Image is uploaded."}, 201
    except UploadNotAllowed:
        extension = image_helper.get_extension(data["image"])
        return {"message": "!!!"}, 400

@app.route('/client/<string:uuid>/image/<string:image>', methods=['GET'])
@cross_origin()
def get_image(uuid, image: str):
    folder = f"user_{uuid}"
    if not image_helper.is_filename_safe(image):
        return {"message": "Name is not safe!"}, 400
    
    try:
        return send_file(image_helper.get_path(image, folder=folder))
    except FileNotFoundError:
        return {"message": "Image does not exist!"}, 404

@app.route('/client/<string:uuid>/image/<string:image>', methods=['DELETE'])
@cross_origin()
def delete_image(uuid, image: str):
    folder = f"user_{uuid}"

    if not image_helper.is_filename_safe(image):
        return {"message": "Name is not safe!"}, 400
    
    try:
        os.remove(image_helper.get_path(image, folder=folder))
        return {"message": "Image was deleted successfuly."}, 200
    except FileNotFoundError:
        return {"message": "Image does not exist!"}, 404
    except:
        traceback.print_exc()
        return {"message": "Image failed to delete!"}, 500

if __name__ == '__main__':
    app.run(debug=True)