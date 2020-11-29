import subprocess
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from ratelimit import UNSAFE as UNSAFE_METHODS
from ratelimit.decorators import ratelimit

from .forms import MetadataRemovalForm


@ratelimit(key="ip", rate="10/m", method=["GET", "HEAD", "OPTIONS", "CONNECT", "TRACE"])
@ratelimit(key="ip", rate="10/h", method=UNSAFE_METHODS, block=True)
def remove_metadata(request):
    if request.method == "POST":
        form = MetadataRemovalForm(request.POST, request.FILES)
        if form.is_valid():
            file_to_clean = request.FILES["file_to_clean"]
            filename = Path(file_to_clean.name)
            save_as = filename.with_name(uuid4().hex + filename.name)
            exts = "".join(filename.suffixes)
            cleaned_filename = filename.with_name(
                filename.name.replace(exts, ".cleaned" + exts)
            )
            tmp_file_path = settings.TEMP_SAVE_FOLDER / save_as
            with tmp_file_path.open("wb+") as tmp_file:
                for chunk in file_to_clean.chunks():
                    tmp_file.write(chunk)
            subprocess.run(["mat2", "--inplace", tmp_file_path])
            try:
                return FileResponse(
                    tmp_file_path.open("rb"),
                    as_attachment=True,
                    filename=cleaned_filename.name,
                )
            finally:
                tmp_file_path.unlink()
    else:
        form = MetadataRemovalForm()
    return render(request, "tools/remove_metadata.html", {"form": form})
