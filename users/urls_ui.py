from django.urls import path
from . import views_ui

urlpatterns = [
    path('', views_ui.login_view, name="ui_login"),
    path('verify/', views_ui.verify_view, name="ui_verify"),
    path('profile/', views_ui.profile_view, name="ui_profile"),
]
