from django.urls import path
from . import views

urlpatterns = [
    path("", views.PaymentGetwaysView.as_view(), name="payment_gateways"),
    path("paypal/", views.payment_paypal, name="paypal"),
    path("payment-succeed/", views.payment_succeed, name="payment-succeed"),
    path("complete/", views.paymentComplete, name="complete"),
    path("create-invoice/", views.create_invoice, name="create_invoice"),
    path("invoice-detail/<int:id>/", views.invoice_detail, name="invoice_detail"),
    path("paiement/ligdicash",views.ligdicash1, name="ligdicash"),
]
