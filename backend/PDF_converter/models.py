import os
from django.db import models
from core.behaivours import Timestampable
from django.core.validators import FileExtensionValidator


class UploadedFile(Timestampable):
    """ Model for storing UploadedFiles """

    file = models.FileField(
        upload_to='Uploaded_Files/pdf_files/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    converted_file = models.FileField(
        upload_to='Uploaded_Files/converted_files/',
        blank=True, null=True
    )

    def __str__(self):
        """ String representation """
        # return self.file
        return os.path.basename(self.file.name)

    class Meta:
        """ Representation in admin panel """
        verbose_name = 'PDF'
        verbose_name_plural = 'PDFs'
