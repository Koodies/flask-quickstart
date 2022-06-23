from marshmallow import fields, Schema


UserSchema = Schema.from_dict({
    'id': fields.Str(required=True),
    'name': fields.Str(required=True)
})
