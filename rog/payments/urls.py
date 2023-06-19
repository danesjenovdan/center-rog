from django.urls import path
from .views import Pay, PaymentDataXML, PaymentSuccess, PaymentFailure, PaymentSuccessXML, InitPay

urlpatterns = [
    path('', Pay.as_view()),
    path('zacni-ujp/', InitPay.as_view()),
    path('narocilo/', PaymentDataXML.as_view()),
    path('uspesno/', PaymentSuccess.as_view()),
    path('neuspesno/', PaymentFailure .as_view()),
    path('potrditev/', PaymentSuccessXML.as_view()),
]
