from flask import jsonify, request
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from myproject import app
from marshmallow import Schema, fields
from myproject.clientmodels import ClientModel, LanguageModel, ContactModel

class LanguageSchema(Schema):
    
    name = fields.String()

class ContactSchema(Schema):
    
    number = fields.Integer()

class ClientSchema(Schema):
    forename = fields.String()
    surname = fields.String()
    email = fields.String()
    homeAddress = fields.String()
    city = fields.String()
    postCode = fields.String()
    languages = fields.Nested(LanguageSchema(only=("name",)), many=True)
    contact_numbers = fields.Nested(ContactSchema(only=("number",)), many=True)