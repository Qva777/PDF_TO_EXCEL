from django.db import models
from core.behaivours import Timestampable


class UploadedFile(Timestampable):
    """ Model for storing UploadedFiles """

    file = models.FileField(upload_to='pdf_files/')
    converted_file = models.FileField(upload_to='converted_files/', blank=True, null=True)

    def __str__(self):
        """ String representation """
        return self.file

    class Meta:
        """ Representation in admin panel """
        verbose_name = 'PDF'
        verbose_name_plural = 'PDFs'
