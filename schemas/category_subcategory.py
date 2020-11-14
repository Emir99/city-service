from marshmallow import Schema, fields


class CategoryImageSchema(Schema):

    path = fields.String()
    extension = fields.String()


class SubCategorySchema(Schema):

    name = fields.String()
    description = fields.String()
    icon_name = fields.String()
    images = fields.Nested(CategoryImageSchema(many=True))


class CategorySchema(Schema):
    name = fields.String()
    description = fields.String()
    icon_name = fields.String()
    images = fields.Nested(CategoryImageSchema(many=True))
    subcategories = fields.Nested(SubCategorySchema(exclude=('description', 'images', 'icon_name')), many=True)
