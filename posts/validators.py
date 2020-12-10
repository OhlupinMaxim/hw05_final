from django import forms

from .models import Group


def validate_not_empty(value):
    if value == "":
        raise forms.ValidationError(
            "Поле, не заполнено!",
            params={"value": value},
        )

