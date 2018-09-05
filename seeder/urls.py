from django.urls import path

from seeder import views

app_name = 'seeder'
urlpatterns = [
    path('', views.index, name='index'),
]
