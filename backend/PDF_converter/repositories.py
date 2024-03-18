from django.shortcuts import get_object_or_404
from PDF_converter.models import UploadedFile


class PDFRepository:
    """ Repository for PDF Models  """

    @staticmethod
    def get_pdf_id(pk):
        """ Get PDF id from Database """
        return get_object_or_404(UploadedFile, pk=pk)
