from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls.authentication')),
    path('', include('accounts.urls.pannel')),
]