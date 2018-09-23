from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),

    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='login'),
    path('register', views.register, name='register'),
    path('forgot', views.forgot, name='forgot'),
    path('recover', views.recover, name='recover'),
    path('user/', views.user, name='user'),
    path('user/<int:group_id>/', views.user, name='usergroup'),
    path('kelas', views.kelas, name='kelas'),
    path('newclass', views.kelasbaru, name='kelasbaru'),
    path('admin', views.admin, name='admin'),
    path('admin/<int:mode_admin>/', views.admin),
    # ex: /polls/5/
    path('kelas/<int:kelas_id>/detail', views.detailkelas, name='detailkelas'),
    path('kelas/<int:kelas_id>/edit', views.editkelas, name='editkelas'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('statistik', views.statistik, name='statistik'),
]
