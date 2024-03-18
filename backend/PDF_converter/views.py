import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from converter_config.settings import API_PDF_TABLES
from pdftables_api import Client

from PDF_converter.repositories import PDFRepository
from PDF_converter.formatter import CSVReader
from PDF_converter.forms import FileUploadForm
from PDF_converter.models import UploadedFile


class FileDetailView(View):
    """ Detail view for uploaded file """

    @staticmethod
    def get(request, pk):
        uploaded_file = PDFRepository.get_pdf_id(pk)
        return render(request, 'download.html', {'uploaded_file': uploaded_file})


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

            # Upload and convert with basename
            output_folder = uploaded_file.converted_file.field.upload_to
            file_name, file_extension = os.path.splitext(uploaded_file.file.name)
            output_filename = f'{os.path.basename(file_name)}.csv'

            # Path to file
            output_path = os.path.join(output_folder, output_filename)

            if not os.path.exists(output_path):
                # Check if file exists, then convert it to csv
                c = Client(API_PDF_TABLES)
                c.csv(uploaded_file.file.path, output_path)
                uploaded_file.converted_file = output_path
                uploaded_file.save()

                # Format the CSV
                CSVReader.open_read_file(output_path)

            return redirect('file_detail', pk=uploaded_file.pk)
        return render(request, 'upload_pdf.html', {'form': form})


class DownloadExcelView(View):
    """ Download CSV table """

    @staticmethod
    def get(request, pk):
        uploaded_file = UploadedFile.objects.get(pk=pk)

        if uploaded_file.converted_file:
            excel_file_path = uploaded_file.converted_file.path

            file_name, file_extension = os.path.splitext(uploaded_file.file.name)
            output_filename = f'{os.path.basename(file_name)}.csv'

            with open(excel_file_path, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                return response
        else:
            return HttpResponse("CSV file not found")
