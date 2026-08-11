from django.urls import path
from .views import credit_sale_list_view

urlpatterns = [
    path('', credit_sale_list_view, name='credit_sale_list'),
]
