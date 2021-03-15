"""payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from payment.views import dashboard, failed_payment, invoice, paytm_handler, razorpay_handler
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('dashboard', csrf_exempt(dashboard), name='dashboard'),
    path('paytm/handler/', csrf_exempt(paytm_handler), name='paytm_handler'),
    path("razorpay/handler/", csrf_exempt(razorpay_handler),
         name="razorpay_handler"),
    path('razorpay/failed', csrf_exempt(failed_payment), name='failed_payment'),
    path('invoice/<str:id>/', invoice, name='invoice'),
]
