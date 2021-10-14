from django.urls import path

from . import views

urlpatterns = [
    # index
    path('', views.index, name='index'),
    # login
    path('login/', views.login, name='login'),
]