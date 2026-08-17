from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.customers.views import CustomerViewSet
from apps.credit.views import CreditSaleViewSet
from apps.payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'credit-sales', CreditSaleViewSet)
router.register(r'payments', PaymentViewSet)

from apps.analytics.views import dashboard

from django.contrib.auth import views as auth_views

from django.http import HttpResponse

def health_check(request):
    return HttpResponse("BakiFlow is running!")

from apps.accounts.views import logout_view, register_view

from apps.intelligence.views import ChatbotAskView

urlpatterns = [
    path('health/', health_check),
    path('', dashboard, name='dashboard'),
    path('api/v1/chatbot/ask/', ChatbotAskView.as_view(), name='chatbot_ask'),
    path('customers/', include('apps.customers.urls')),
    path('credit/', include('apps.credit.urls')),
    path('payments/', include('apps.payments.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/register/', register_view, name='register'),
]
