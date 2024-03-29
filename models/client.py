from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ClientModel(db.Model):
    __tablename__ = 'clients'

    identifier = db.Column(db.String, primary_key=True, nullable=False, index=True)
    forename = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    home_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    post_code = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    residency = db.Column(db.String, nullable=False)
    email_confirmation = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(10), nullable=False)

    languages = db.relationship('ClientLanguageModel', cascade='all,delete',
                                backref='clients', lazy='dynamic')

    contact_numbers = db.relationship('ClientContactModel', cascade='all,delete',
                                      backref='clients', lazy='dynamic')

    images = db.relationship('ClientImageModel', cascade='all,delete',
                             backref='clients', lazy='dynamic')

    def __init__(self, identifier, forename, surname, email, home_address, city, post_code,
                 dob, residency, email_confirmation, role):
        self.identifier = identifier
        self.forename = forename
        self.surname = surname
        self.email = email
        self.home_address = home_address
        self.city = city
        self.post_code = post_code
        self.dob = dob
        self.residency = residency
        self.email_confirmation = email_confirmation
        self.role = role

    @classmethod
    def find_by_identifier(cls, identifier):
        return cls.query.filter_by(identifier=identifier).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ClientLanguageModel(db.Model):

    __tablename__ = 'client_languages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    name = db.Column(db.String)
    client_id = db.Column(db.String, db.ForeignKey('clients.identifier'), nullable=False)

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

    @classmethod
    def find_lang_by_client_id(cls, client_id):
        return cls.query.filter(cls.client_id == client_id).all()


class ClientContactModel(db.Model):

    __tablename__ = 'client_contacts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    number = db.Column(db.Integer)
    client_id = db.Column(db.String, db.ForeignKey('clients.identifier'), nullable=False)

    def __init__(self, number, client_id):
        self.number = number
        self.client_id = client_id

    @classmethod
    def find_cont_by_client_id(cls, client_id):
        return cls.query.filter(cls.client_id == client_id).all()


class ClientImageModel(db.Model):

    __tablename__ = 'client_images'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    path = db.Column(db.String, unique=True, nullable=False, index=True)
    extension = db.Column(db.String, nullable=False, index=True)

    client_id = db.Column(db.String, db.ForeignKey('clients.identifier'), nullable=False)

    def __init__(self, path, extension, client_id):
        self.path = path
        self.extension = extension
        self.client_id = client_id

    @classmethod
    def find_image_by_client_id(cls, client_id):
        return cls.query.filter(cls.client_id == client_id).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
