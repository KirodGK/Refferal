from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('ui/', include('users.urls_ui')),
]