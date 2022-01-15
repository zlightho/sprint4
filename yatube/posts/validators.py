# validators.py
from django import forms


# Функция-валидатор:
def validate_not_empty(value):
    # Проверка "а заполнено ли поле?"
    if value == "":
        raise forms.ValidationError(
            "Заполните поле?",
            params={"value": value},
        )
