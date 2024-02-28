import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from PDF_converter.repositories import PDFRepository
from converter_config.settings import API_PDF_TABLES
from pdftables_api import Client
from PDF_converter.forms import FileUploadForm


class UploadFileView(View):
    """ View to upload a PDF file """

    @staticmethod
    def get(request):
        form = FileUploadForm()
        return render(request, 'upload_pdf.html', {'form': form})

    @staticmethod
    def post(request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            output_folder = 'converted_files'
            output_filename = 'output.xlsx'
            output_path = os.path.join(output_folder, output_filename)

            c = Client(API_PDF_TABLES)
            c.xlsx(uploaded_file.file.path, output_path)

            uploaded_file.converted_file = output_path
            uploaded_file.save()

            return redirect('file_detail', pk=uploaded_file.pk)
        return render(request, 'upload_pdf.html', {'form': form})


class FileDetailView(View):
    """ Detail view for uploaded file """

    @staticmethod
    def get(request, pk):
        uploaded_file = PDFRepository.get_pdf_id(pk)
        return render(request, 'download.html', {'uploaded_file': uploaded_file})


class DownloadExcelView(View):
    """ Download excel table """

    @staticmethod
    def get(request, pk):
        uploaded_file = PDFRepository.get_pdf_id(pk)

        if uploaded_file.converted_file:
            excel_file_path = uploaded_file.converted_file.path
            with open(excel_file_path, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(excel_file_path)}"'
                return response
        else:
            return HttpResponse("Excel file not found")
