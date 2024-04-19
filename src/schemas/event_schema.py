from marshmallow import Schema, fields, validate, post_load
from src.models import EventModel


class EventSchema(Schema):
    '''
    Esquema de la entidad Event para serializar y deserializar formato json.

    param:
        - Schema: Clase de la cual hereda    
    '''
    id = fields.Int(dump_only=True)
    date = fields.DateTime(required=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=True, validate=validate.Length(max=100))
    location = fields.Str(required=True, validate=validate.Length(max=50))
    capacity = fields.Int(required=True)
    organizer = fields.Str(required=True, validate=validate.Length(max=50))

    @post_load
    def make_event(self, data, **kwargs):
        '''
        Función que crea un objeto de tipo EventModel a partir de un diccionario

        args:
            - data: diccionario con los datos del curso
        return:
            - Objeto de tipo EventModel
        '''
        return EventModel(**data)