from django.core.exceptions import ValidationError


def humanize_bytes(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, fileobj):
        fileobj.seek(0, 2)
        file_size = fileobj.tell()
        if file_size > self.max_size:
            raise ValidationError(
                message=f"Tamanho máximo do arquivo é {humanize_bytes(self.max_size)}."
            )
