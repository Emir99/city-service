from db import db
from sqlalchemy.dialects.postgresql import UUID

connect_provider_category = db.Table('provider_req_category',
                                     db.Column('provider_req_id', db.String,
                                               db.ForeignKey('provider_req.identifier')),
                                     db.Column('category_id', UUID(as_uuid=True),
                                               db.ForeignKey('category.id')))

connect_provider_subcategory = db.Table('provider_req_subcategory',
                                        db.Column('provider_req_id', db.String,
                                                  db.ForeignKey('provider_req.identifier')),
                                        db.Column('subcategory_id', UUID(as_uuid=True),
                                                  db.ForeignKey('subcategory.id')))

mesh_provider_category = db.Table('provider_category',
                                  db.Column('provider_id', db.String,
                                            db.ForeignKey('provider.identifier')),
                                  db.Column('category_id', UUID(as_uuid=True),
                                            db.ForeignKey('category.id')))

mesh_provider_subcategory = db.Table('provider_subcategory',
                                     db.Column('provider_id', db.String,
                                               db.ForeignKey('provider.identifier')),
                                     db.Column('subcategory_id', UUID(as_uuid=True),
                                               db.ForeignKey('subcategory.id')))
