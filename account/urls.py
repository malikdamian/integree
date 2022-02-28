from django.urls import path, include

from account.views import dashboard, add_user

urlpatterns = [
    path('add/', add_user, name='add_user'),
    path('', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),

]
