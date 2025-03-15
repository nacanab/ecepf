from django.urls import path

from activationkey import api_view

urlpatterns =[
    path('validate-activation-key/',api_view.ValidateActivationKeyView.as_view(),name='activation_validate'),
    path('generate-activation-key/',api_view.ActivateDeviceView.as_view(),name='activation_generate'),
]