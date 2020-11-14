from marshmallow import Schema, fields


class ProviderLanguageSchema(Schema):
    name = fields.String()


class ProviderContactSchema(Schema):
    number = fields.Integer()


class ProviderImageSchema(Schema):
    path = fields.String()
    extension = fields.String()


class ProviderSchema(Schema):
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
    status = fields.String()

    occupations = fields.List(fields.Nested("CategorySchema",
                                            exclude=("description", "subcategories", "icon_name", "images")),
                              many=True)
    subcategories = fields.List(fields.Nested("SubCategorySchema",
                                              exclude=("description", "images", "icon_name")), many=True)

    languages = fields.Nested(ProviderLanguageSchema(only=("name",)), many=True)
    contact_numbers = fields.Nested(ProviderContactSchema(only=("number",)), many=True)
    images = fields.Nested(ProviderImageSchema(many=True))
