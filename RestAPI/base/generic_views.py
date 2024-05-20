"""Base Mixins for the project.
"""
from django.views import View
from django.utils.translation import gettext as _
from django.http import HttpRequest, JsonResponse

from .logger import base_logger
from .http_status_codes import HTTP_STATUS as status

from .mixins import BaseMixin


class BaseListView(BaseMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        Base List Get View

        Returns the list of the objects given the information in the GET
        request.
        """
        try:
            query_set = self.filter_query(request.GET)
            data = {
                    self.model._meta.verbose_name_plural: self.serialize(query_set),
            }
            return JsonResponse(data, status=status.ok)
        except Exception as e:
            error_data = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseCreateView(BaseMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Base Post View

        Creates a db object given the form data in the POST request.
        """
        try:
            created_object = self.create_object(data=request.POST)
            msg = {
                self.model._meta.verbose_name: self.serialize(created_object),
            }
            return JsonResponse(msg, status=status.created)
        except Exception as e:
            error_data = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseDetailView(BaseMixin, View):
    url_kwarg: str = "id"

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Base Detailed Get View

        Returns the db object given the url_kwarg identifier.
        """
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object = self.get_query(data=data)
            msg = {
                self.model._meta.verbose_name: self.serialize(db_object),
            }
            return JsonResponse(msg, status=status.accepted)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseUpdateView(BaseMixin, View):
    url_kwarg: str = "id"

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Base Update View

        Updates the db object given the url_kwarg identifier and the form data
        in the POST request.
        """
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object = self.get_query(data=data)
            db_object = self.update_object(
                db_object=db_object,
                data=request.POST,
            )
            msg = {
                self.model._meta.verbose_name: self.serialize(db_object),
            }
            return JsonResponse(msg, status=status.accepted)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseDeleteView(BaseMixin, View):
    url_kwarg: str = "id"

    def delete(self, request: HttpRequest, *args, **kwargs):
        """
        Base Delete View

        Deletes the db object given the url_kwarg identifier.
        """
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object = self.get_query(data=data)
            self.delete_object(db_object=db_object)
            msg = {
                "response": f"{self.model._meta.verbose_name} has been deleted."
            }
            return JsonResponse(msg, status=status.accepted)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": "Internal server error."
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)
