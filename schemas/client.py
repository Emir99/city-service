from marshmallow import Schema, fields


class ClientLanguageSchema(Schema):

    name = fields.String()


class ClientContactSchema(Schema):

    number = fields.Integer()


class ClientSchema(Schema):
    forename = fields.String()
    surname = fields.String()
    email = fields.String()
    home_address = fields.String()
    city = fields.String()
    post_code = fields.String()
    languages = fields.Nested(ClientLanguageSchema(only=("name",)), many=True)
    contact_numbers = fields.Nested(ClientContactSchema(only=("number",)), many=True)
