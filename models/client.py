from db import db


class ClientModel(db.Model):

    __tablename__ = 'clients'

    uuid = db.Column(db.String, primary_key=True)
    forename = db.Column(db.String(30), index=True)
    surname = db.Column(db.String(30), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    home_address = db.Column(db.String, index=True)
    city = db.Column(db.String(50), index=True)
    post_code = db.Column(db.String, index=True)

    languages = db.relationship('ClientLanguageModel', backref='client', lazy='joined')
    contact_numbers = db.relationship('ClientContactModel', backref='client', lazy='joined')

    def __init__(self, uuid, forename, surname, email, home_address, city, post_code):
        self.uuid = uuid
        self.forename = forename
        self.surname = surname
        self.email = email
        self.home_address = home_address
        self.city = city
        self.post_code = post_code

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ClientLanguageModel(db.Model):

    __tablename__ = 'client_languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    client_id = db.Column(db.String, db.ForeignKey('clients.uuid'))

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

    @classmethod
    def find_lang_by_client_id(cls, client_id):
        return cls.query.filter(cls.client_id == client_id).all()


class ClientContactModel(db.Model):

    __tablename__ = 'client_contacts'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    client_id = db.Column(db.String, db.ForeignKey('clients.uuid'))

    def __init__(self, number, client_id):
        self.number = number
        self.client_id = client_id

    @classmethod
    def find_num_by_client_id(cls, client_id):
        return cls.query.filter(cls.client_id == client_id).all()
