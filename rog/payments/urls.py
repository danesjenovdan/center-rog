from django.urls import path
from .views import (
    Pay,
    PaymentDataXML,
    PaymentSuccess,
    PaymentFailure,
    PaymentSuccessXML,
    PaymentHistory,
    PaymentInvoice,
    PaymentPreview
)

urlpatterns = [
    path('', PaymentPreview.as_view(), name='preview'),
    path('izvedi/', Pay.as_view(), name='pay'),
    path('narocilo/', PaymentDataXML.as_view()),
    path('uspesno/', PaymentSuccess.as_view()),
    path('neuspesno/', PaymentFailure .as_view()),
    path('potrditev/', PaymentSuccessXML.as_view()),
    path('zgodovina/', PaymentHistory.as_view(), name='history'),
    path('racun/<int:payment_id>/', PaymentInvoice.as_view(), name='invoice')
]
