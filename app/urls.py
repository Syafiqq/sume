from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),

    path('login', views.dologin, name='login'),
    path('register', views.register, name='register'),
    path('user', views.user, name='user'),
    path('kelas', views.kelas, name='kelas'),
    path('admin', views.admin, name='admin'),
    # ex: /polls/5/
    path('detail/<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
