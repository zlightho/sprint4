import datetime

now = datetime.datetime.now()
current_year = now.year


def year(request):
    """Добавляет переменную с текущим годом."""
    return {"year": current_year}
