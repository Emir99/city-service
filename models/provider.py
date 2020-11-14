from db import db
from models.provider_category import mesh_provider_category, mesh_provider_subcategory
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ProviderModel(db.Model):
    __tablename__ = 'provider'

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

    occupations = db.relationship('CategoryModel', secondary=mesh_provider_category,
                                  backref=db.backref('categories', lazy='dynamic'))

    subcategories = db.relationship('SubCategoryModel', secondary=mesh_provider_subcategory,
                                    backref=db.backref('subcategories', lazy='dynamic'))

    languages = db.relationship('ProviderLanguageModel', cascade='all,delete',
                                backref='provider', lazy='dynamic')

    contact_numbers = db.relationship('ProviderContactModel', cascade='all,delete',
                                      backref='provider', lazy='dynamic')

    images = db.relationship('ProviderImageModel', cascade='all,delete',
                             backref='provider', lazy='dynamic')

    personal = db.relationship('ProviderPersonal', cascade='all,delete',
                               backref='provider', uselist=False)

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


class ProviderLanguageModel(db.Model):

    __tablename__ = 'provider_languages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    name = db.Column(db.String)
    provider_id = db.Column(db.String, db.ForeignKey('provider.identifier'), nullable=False)

    def __init__(self, name, provider_id):
        self.name = name
        self.provider_id = provider_id

    @classmethod
    def find_lang_by_provider_id(cls, provider_id):
        return cls.query.filter(cls.provider_id == provider_id).all()


class ProviderContactModel(db.Model):

    __tablename__ = 'provider_contacts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    number = db.Column(db.Integer)
    provider_id = db.Column(db.String, db.ForeignKey('provider.identifier'), nullable=False)

    def __init__(self, number, provider_id):
        self.number = number
        self.provider_id = provider_id

    @classmethod
    def find_cont_by_provider_id(cls, provider_id):
        return cls.query.filter(cls.provider_id == provider_id).all()


class ProviderImageModel(db.Model):

    __tablename__ = 'provider_images'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    path = db.Column(db.String, unique=True, nullable=False, index=True)
    extension = db.Column(db.String, nullable=False, index=True)

    provider_id = db.Column(db.String, db.ForeignKey('provider.identifier'), nullable=False)

    def __init__(self, path, extension, provider_id):
        self.path = path
        self.extension = extension
        self.provider_id = provider_id

    @classmethod
    def find_image_by_provider_id(cls, provider_id):
        return cls.query.filter(cls.provider_id == provider_id).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ProviderPersonal(db.Model):
    __tablename__ = 'provider_personal'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    number = db.Column(db.Integer)
    provider_id = db.Column(db.String, db.ForeignKey('provider.identifier'), nullable=False)

    def __init__(self, number, provider_id):
        self.number = number
        self.provider_id = provider_id

    @classmethod
    def find_cont_by_provider_id(cls, provider_id):
        return cls.query.filter(cls.provider_id == provider_id).all()
