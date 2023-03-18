from django.core.exceptions import ValidationError

from room.tasks import validate_html_tag


def my_websocket_handler(message):
    errors = []
    try:
        validate_html_tag(message)
    except ValidationError as e:
        errors.append(e.message)
    return errors
