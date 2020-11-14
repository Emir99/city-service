from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class SubCategoryModel(db.Model):

    __tablename__ = 'subcategory'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    name = db.Column(db.String, unique=True, nullable=False, index=True)
    description = db.Column(db.String)
    icon_name = db.Column(db.String)

    images = db.relationship('SubCategoryImageModel', cascade='all,delete', backref='subcategory', lazy='dynamic')

    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))

    def __init__(self, name, description, icon_name, category_id):
        self.name = name
        self.description = description
        self.icon_name = icon_name
        self.category_id = category_id

    @classmethod
    def find_sub_by_category_id(cls, category_id):
        return cls.query.filter(cls.category_id == category_id).all()

    @classmethod
    def find_sub_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class SubCategoryImageModel(db.Model):

    __tablename__ = 'subcategory_images'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    path = db.Column(db.String, unique=True, nullable=False, index=True)
    extension = db.Column(db.String, nullable=False, index=True)

    subcategory_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subcategory.id'))

    def __init__(self, path, extension, subcategory_id):
        self.path = path
        self.extension = extension
        self.subcategory_id = subcategory_id

    @classmethod
    def find_image_by_subcategory_id(cls, subcategory_id):
        return cls.query.filter(cls.subcategory_id == subcategory_id).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
