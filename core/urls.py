from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('auth', auth, name='auth'),
    path('mint', mint, name='mint'),
    path('getprice', getprice, name='getprice'),
    path('freedice', FreeDice.as_view()),
    path('premiumdice', PremiumDice.as_view())
]