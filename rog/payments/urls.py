from django.urls import path
from .views import (
    Pay,
    PaymentDataXML,
    PaymentSuccess,
    PaymentFailure,
    PaymentSuccessXML,
    PaymentHistory
)

urlpatterns = [
    path('', Pay.as_view()),
    path('narocilo/', PaymentDataXML.as_view()),
    path('uspesno/', PaymentSuccess.as_view()),
    path('neuspesno/', PaymentFailure .as_view()),
    path('potrditev/', PaymentSuccessXML.as_view()),
    path('zgodovina/', PaymentHistory.as_view()),
]
