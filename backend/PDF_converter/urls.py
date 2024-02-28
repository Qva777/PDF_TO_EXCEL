from django.urls import path
from PDF_converter import views

urlpatterns = [
    # Upload PDF File
    path('', views.UploadFileView.as_view(), name='upload_file'),

    # Detail PDF view
    path('file/<uuid:pk>/', views.FileDetailView.as_view(), name='file_detail'),

    # Download Excel page
    path('file/<uuid:pk>/download_excel/', views.DownloadExcelView.as_view(), name='download_excel'),
]
