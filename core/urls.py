from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('auth', auth, name='auth'),
    path('mint', mint, name='mint'),
    path('getprice', getprice, name='getprice'),
    path('creating/', creating, name='creating'),
    path('ownership/', ownership, name='ownership'),
    path('getcost/<str:address>/', cost),
]