from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class CategoryModel(db.Model):

    __tablename__ = 'category'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    name = db.Column(db.String,  unique=True, nullable=False, index=True)
    description = db.Column(db.String)
    icon_name = db.Column(db.String)

    images = db.relationship('CategoryImageModel', cascade='all,delete', backref='category', lazy='dynamic')
    subcategories = db.relationship('SubCategoryModel', cascade='all,delete', backref='category', lazy='dynamic')

    def __init__(self, name, description, icon_name):
        self.name = name
        self.description = description
        self.icon_name = icon_name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class CategoryImageModel(db.Model):

    __tablename__ = 'category_images'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    path = db.Column(db.String, unique=True, nullable=False, index=True)
    extension = db.Column(db.String, nullable=False, index=True)

    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))

    def __init__(self, path, extension, category_id):
        self.path = path
        self.extension = extension
        self.category_id = category_id

    @classmethod
    def find_image_by_category_id(cls, category_id):
        return cls.query.filter(cls.category_id == category_id).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
