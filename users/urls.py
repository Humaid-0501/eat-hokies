from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    # dining_list views
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/edit/<str:username>', views.profile_edit, name='profile_edit'),
    path('edit/details/<str:username>', views.edit_detail, name='edit_detail'),
    path('login', views.login_user, name='login'),
    path('login/page', views.login_page, name='login_page'),
    path('logout', views.logout_user, name='logout'),
]