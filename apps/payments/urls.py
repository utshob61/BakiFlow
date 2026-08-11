from django.urls import path
from .views import payment_list_view

urlpatterns = [
    path('', payment_list_view, name='payment_list'),
]
