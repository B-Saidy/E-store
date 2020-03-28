from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='stripe'),
    path('charge/', views.charge, name='charge'),
]