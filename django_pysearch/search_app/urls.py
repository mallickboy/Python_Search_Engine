from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Should match your home view
    path('search/', views.search, name='search'),
]
