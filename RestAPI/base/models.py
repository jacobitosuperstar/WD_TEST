from typing import (
    Dict,
    Any,
)
from django.db import models


class BaseModel(models.Model):
    """Base fields that all database models should have.

    Fields
    ------
    created_at: DateTime
        Creation time of the row.
    updated_at: DateTime
        Updated time of the row.
    is_deleted: Bool
        Soft deletion of the element of the row.
    """
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    deleted = models.BooleanField(default=False,)

    class Meta:
        abstract = True

    def serializer(self, depth: int = 0) -> Dict[str, Any]:
        """Returns a dict object with the corresponding fields and values that
        you want to serialize.
        """
        # get the model of the object
        model = self._meta.model

        # getting the fields of the model. We skip over the fields that are of
        # type one_to_many.
        fields = [
            field for field in model._meta.get_fields()
            if not field.one_to_one
        ]

        # This is where we are going to store the fields and the values of the
        # object
        serialized_object = {}

        for field in fields:

            field_name = field.name
            field_value = getattr(self, field_name)

            # changing the datatime to ISO format
            if isinstance(field, (models.DateTimeField, models.DateField)):
                field_value = field_value.isoformat() if field_value else None

            # the resulting object is not a simple type, so we need to
            # serialize again.
            if isinstance(field, models.OneToOneField):
                if depth > 0:
                    field_value = field_value.serializer(depth=depth-1)
                else:
                    field_value = field_value.id
            serialized_object[field_name] = field_value
        return serialized_object
