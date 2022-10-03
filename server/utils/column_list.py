from django.db.models import ManyToOneRel
from django.db.models.fields import BooleanField

def get_column_list(serializer_fields_list, fields_list):
    column_dict_list = []
    column_list = []
    for field in fields_list:
        if not isinstance(field, ManyToOneRel) and (field.name in serializer_fields_list or serializer_fields_list == '__all__'):
            column = {'prop': field.name, 'label': field.verbose_name, 'is_boolean_field': isinstance(field, BooleanField)}
            column_dict_list.append(column)
            column_list.append(field.name)
    if serializer_fields_list != '__all__':
        for field in serializer_fields_list:
            if field not in column_list:
                column = {'prop': field, 'label': field, 'is_boolean_field': False}
                column_dict_list.append(column)

    return column_dict_list