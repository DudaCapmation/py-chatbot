from django.urls import path
from .views import process_unstructured

urlpatterns = [
    path("process/", process_unstructured, name = "process_unstructured"),
]