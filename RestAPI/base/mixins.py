"""Base Mixins for the project.
"""
from typing import (
    Dict,
    List,
    Union,
    Any,
)
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .logger import base_logger
from .models import BaseModel


class BaseMixin:
    model: BaseModel
    serializer_depth: int = 0

    def serialize(
        self,
        objects: Union[QuerySet, BaseModel],
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Serializer of the different objects that we are working with. If its a
        `Queryset` what is passed, a list of each element serialized will be
        returned. If is a `BaseModel` type object, just the serialized item
        will be returned.
        """
        if isinstance(objects, QuerySet):
            serialized_objects = [element.serializer(depth=self.serializer_depth) for element in objects]
        elif isinstance(objects, BaseModel):
            serialized_objects = objects.serializer(depth=self.serializer_depth)
        else:
            raise NotImplementedError("The `Type` that you are passing won't be processed.")
        return serialized_objects

    def filter_query(
        self,
        data: Dict[str, Any],
    ) -> QuerySet:
        """Dinamically created filtering query given the data.
        """
        query = Q()

        for key, value in data.items():
            # validating that they key passed is actually in the model fields
            fields = [
                field.name for field in self.model._meta.get_fields()
            ]
            if key in fields:
                query &= Q(**{key:value})

        queryset: QuerySet = self.model.objects.filter(query)
        return queryset

    def get_query(
        self,
        data: Dict[str, Any]
    ) -> BaseModel:
        """Dinamically created get query, given the data.
        """
        query = Q()

        for key, value in data.items():
            # validating that they key passed is actually in the model fields
            fields = [
                field.name for field in self.model._meta.get_fields()
            ]
            if key in fields:
                query &= Q(**{key:value})

        try:
            db_object: BaseModel = self.model.objects.get(query)
            return db_object
        except self.model.DoesNotExist as e:
            msg = {
                "response": f"{self.model._meta.verbose_name} not found."
            }
            raise ObjectDoesNotExist(msg)
        except Exception as e:
            msg = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            raise Exception(msg)

    def create_object(self, data: Dict) -> BaseModel:
        """Creates a model object with the given cleaned data.
        """
        try:
            model_object: BaseModel = self.model()

            for key, value in data.items():
                if hasattr(model_object, key):
                    setattr(model_object, key, value)

            model_object.full_clean()
            model_object.save()
            return model_object
        except Exception as e:
            # Handle validation or database constraint errors
            msg = {
                "response": f"Error creating object {self.model._meta.verbose_name}"
            }
            base_logger.critical(e)
            raise Exception(msg)

    def update_object(self, data: Dict, db_object: BaseModel) -> BaseModel:
        """Updates a model object with the given cleaned data.
        """
        try:
            changed = False

            for key, value in data.items():
                if value is not None and hasattr(db_object, key):
                    model_object_value = getattr(db_object, key)
                    if model_object_value != value:
                        setattr(db_object, key, value)
                        changed = True

            if changed is True:
                db_object.full_clean()
                db_object.save()
            return db_object
        except Exception as e:
            # Handle validation or database constraint errors
            msg = {
                "response": f"Error updating object {self.model._meta.verbose_name}"
            }
            base_logger.critical(e)
            raise Exception(msg)

    def delete_object(self, db_object: BaseModel):
        """Updates a model object with the given cleaned data.
        """
        try:
            db_object.deleted = True
            db_object.save()
        except Exception as e:
            # Handle validation or database constraint errors
            msg = {
                "response": f"Error deleting object {self.model._meta.verbose_name}"
            }
            base_logger.critical(e)
            raise Exception(msg)
