from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from usuarios.views import * 


urlpatterns = [
    path("login/", LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="usuarios/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile_detail, name="profile_detail"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("profile/delete/", profile_delete, name="profile_delete"),
]   