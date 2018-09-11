from django.urls import path

from organization import views

app_name = 'organization'
urlpatterns = [
    path('', views.index, name='index'),
]
