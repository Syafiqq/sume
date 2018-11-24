from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    # Landing Page
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='login'),
    path('register', views.register, name='register'),
    path('forgot', views.forgot, name='forgot'),
    path('recover', views.recover, name='recover'),

    # User Management
    path('user/', views.user, name='user'),
    path('user/<int:group_id>/', views.user, name='usergroup'),
    path('admin', views.admin, name='admin'),
    path('admin/<int:mode_admin>/', views.admin),

    # Data
    path('data_latih', views.data_latih, name='data_latih'),
    path('data_uji', views.data_uji, name='data_uji'),
    path('data/upload', views.data_upload, name='data_upload'),
    path('data/view_data/<int:data_id>', views.view_data, name='view_data'),
    path('data/edit_data/<int:data_id>', views.edit_data, name='edit_data'),

    # Class Management
    path('kelas', views.kelas, name='kelas'),
    path('newclass', views.kelasbaru, name='kelasbaru'),
    path('kelas/<int:kelas_id>/detail', views.detailkelas, name='detailkelas'),
    path('kelas/<int:kelas_id>/edit', views.editkelas, name='editkelas'),
    path('kelas/<int:kelas_id>/upload', views.upload_dokumen, name='upload_dokumen'),
    path('kelas/<int:kelas_id>/hapus', views.hapus_kelas, name='hapuskelas'),
    path('kelas/<int:kelas_id>/view_doc/<int:dokumen_id>', views.view_dokumen, name='upload_dokumen'),
    path('view_doc/<int:dokumen_id>', views.view_dokumen, name='view_dokumen'),

    path('statistik', views.statistik, name='statistik'),
]
