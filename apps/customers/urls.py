from django.urls import path
from .views import customer_list_view

urlpatterns = [
    path('', customer_list_view, name='customer_list'),
]
