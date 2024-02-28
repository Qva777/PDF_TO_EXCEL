from django import forms
from PDF_converter.models import UploadedFile


class FileUploadForm(forms.ModelForm):
    """ Form for uploading PDF """

    class Meta:
        model = UploadedFile
        fields = ['file']
