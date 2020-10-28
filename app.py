from myproject import app, db
from flask import jsonify, request
from myproject.clientmodels import ClientModel, LanguageModel, ContactModel
from myproject.clientschemas import ClientSchema, LanguageSchema, ContactSchema

language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@app.route('/client', methods=['POST'])
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
def get_all_clients():
    all_clients = ClientModel.query.all()
    result = clients_schema.dump(all_clients)

    return jsonify(result)  

@app.route('/client/<string:uuid>', methods=['GET'])
def getclient_by_uuid(uuid):
    client = ClientModel.find_by_uuid(uuid)
    result = client_schema.dump(client)
    return jsonify(result)

@app.route('/client/<string:uuid>', methods=['PUT'])
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
def delete_client(uuid):
    client = ClientModel.find_by_uuid(uuid)
    delete = ClientModel.delete_from_db(client)

    return jsonify({'message': 'client deleted'})

@app.route('/client/language/<string:uuid>', methods=['POST'])
def add_lang(uuid):
    lang = request.get_json()
    for i in range(len(lang)):
        name = request.json[i]['name']
        my_language = LanguageModel(name, uuid)
        db.session.add(my_language)

    db.session.commit()
    return jsonify({'message': 'Language is added'})

@app.route('/client/number/<string:uuid>', methods=['POST'])
def add_num(uuid):
    num = request.get_json()
    for i in range(len(num)):
        number = request.json[i]['number']
        my_number = ContactModel(number, uuid)
        db.session.add(my_number)

    db.session.commit()
    return jsonify({'message': 'Number is added'})

if __name__ == '__main__':
    app.run(debug=True)