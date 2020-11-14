from marshmallow import Schema, fields


class ProviderLanguageSchemaReq(Schema):
    name = fields.String()


class ProviderContactSchemaReq(Schema):
    number = fields.Integer()


class ProviderImageSchemaReq(Schema):
    path = fields.String()
    extension = fields.String()


class ProviderSchemaReq(Schema):
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

    languages = fields.Nested(ProviderLanguageSchemaReq(only=("name",)), many=True)
    contact_numbers = fields.Nested(ProviderContactSchemaReq(only=("number",)), many=True)
    images = fields.Nested(ProviderImageSchemaReq(many=True))
