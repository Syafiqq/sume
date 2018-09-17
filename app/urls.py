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
    path('admin', views.admin, name='admin'),
    path('admin/<int:mode_admin>/', views.admin),
    # ex: /polls/5/
    path('detail/<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('statistik', views.statistik, name='statistik')
]
