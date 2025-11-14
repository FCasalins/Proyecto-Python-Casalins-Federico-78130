from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from usuarios.views import * 


urlpatterns = [
    path("login/", LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="usuarios/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile_detail, name="profile_detail"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("profile/delete/", profile_delete, name="profile_delete"),

    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="usuarios/password_change_form.html",
            success_url="/password_change/done/"
        ),
        name="password_change"
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="usuarios/password_change_done.html"
        ),
        name="password_change_done"
    ),
]   