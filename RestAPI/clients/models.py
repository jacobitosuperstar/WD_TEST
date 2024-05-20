from base.models import BaseModel
from django.db import models


class Client(BaseModel):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        max_length=250,
        null=False,
        blank=False,
    )
    cellphone = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "clients"
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self) -> str:
        return f"name: {self.name}"
