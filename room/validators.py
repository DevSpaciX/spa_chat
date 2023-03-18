import os
import re

from PIL import Image
from django.core.exceptions import ValidationError



def my_websocket_handler(message):
    errors = []
    try:
        validate_html_tag(message)
    except ValidationError as e:
        errors.append(e.message)
    return errors


def validate_html_tag(value):
    allowed_tags = ["a", "code", "i", "strong"]
    pattern = re.compile(r"<(/)?\w+[^>]*>")

    value = re.escape(value)
    match = pattern.search(value)
    if match:
        tag, closing = match.group(0), match.group(1)
        if tag[1:-1] not in allowed_tags:
            raise ValidationError(f"Invalid HTML tag: {tag}")
        elif closing:
            if tag[1:-1] not in allowed_tags:
                raise ValidationError(f"Invalid HTML tag: {tag}")
        elif value.count(f"<{tag[1:-1]}>") != value.count(f"</{tag[1:-1]}>"):
            raise ValidationError(f"Unclosed HTML tag: {tag}")



def validate_file(file_path):
    errors = []
    max_image_size = (320, 240)
    max_file_size = 100 * 1024  # 100 KB
    allowed_image_formats = [".jpg", ".jpeg", ".gif", ".png"]
    allowed_text_formats = [".txt"]

    file_ext = os.path.splitext(file_path)[-1].lower()

    if file_ext in allowed_image_formats:
        with Image.open(file_path) as img:
            if img.size[0] > max_image_size[0] or img.size[1] > max_image_size[1]:
                img.thumbnail(max_image_size)
                img.save(file_path)

    elif file_ext in allowed_text_formats:
        if os.path.getsize(file_path) > max_file_size:
            errors.append("Text file size too large.")

    else:
        errors.append("File format not allowed.")

    return errors