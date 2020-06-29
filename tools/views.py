from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from ratelimit.decorators import ratelimit
from ratelimit import UNSAFE as UNSAFE_METHODS
from .forms import MetadataRemovalForm
from uuid import uuid4
import os
import subprocess


@ratelimit(key="ip", rate="10/m", method=["GET", "HEAD", "OPTIONS", "CONNECT", "TRACE"])
@ratelimit(key="ip", rate="10/h", method=UNSAFE_METHODS, block=True)
def remove_metadata(request):
    if request.method == "POST":
        form = MetadataRemovalForm(request.POST, request.FILES)
        if form.is_valid():
            file_to_clean = request.FILES["file_to_clean"]
            save_as = uuid4().hex + file_to_clean.name
            filename, extension = os.path.splitext(file_to_clean.name)
            tmp_file_path = os.path.join(settings.TEMP_SAVE_FOLDER, save_as)
            with open(tmp_file_path, "wb+") as tmp_file:
                for chunk in file_to_clean.chunks():
                    tmp_file.write(chunk)
            subprocess.run(["mat2", "--inplace", tmp_file_path])
            try:
                return FileResponse(open(tmp_file_path, "rb"), as_attachment=True, filename=filename+".cleaned"+extension)
            finally:
                os.remove(tmp_file_path)
    else:
        form = MetadataRemovalForm()
    return render(request, "tools/remove_metadata.html", {"form": form})
