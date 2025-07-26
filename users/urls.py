from django.urls import path
from .views import RequestCodeView, VerifyCodeView, ProfileView

urlpatterns = [
    path('auth/request_code/', RequestCodeView.as_view()),
    path('auth/verify_code/', VerifyCodeView.as_view()),
    path('profile/', ProfileView.as_view()),
]
