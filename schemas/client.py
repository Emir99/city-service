from marshmallow import Schema, fields


class ClientLanguageSchema(Schema):

    name = fields.String()


class ClientContactSchema(Schema):

    number = fields.Integer()


class ClientImageSchema(Schema):

    path = fields.String()
    extension = fields.String()


class ClientSchema(Schema):

    identifier = fields.String()
    forename = fields.String()
    surname = fields.String()
    email = fields.String()
    home_address = fields.String()
    city = fields.String()
    post_code = fields.String()
    dob = fields.String()
    residency = fields.String()
    email_confirmation = fields.Boolean()
    role = fields.String()

    languages = fields.Nested(ClientLanguageSchema(only=("name",)), many=True)
    contact_numbers = fields.Nested(ClientContactSchema(only=("number",)), many=True)
    images = fields.Nested(ClientImageSchema(many=True))
