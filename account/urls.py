from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path

from .forms import UserLoginForm, PasswordResetForm, PasswordResetConfirmForm
from . import views

app_name = "account"

urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="account/registration/login.html", form_class=UserLoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/account/login"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
    path(
        "activate/<slug:uidb64>/<slug:token>",
        views.activate_account,
        name="activate_account",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/user/password_reset_form.html",
            success_url="password_reset_confirmation_email",
            email_template_name="account/user/password_reset_email.html",
            form_class=PasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset_confirmation/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/user/password_reset_confirmation.html",
            success_url="/account/password_reset_complete/",
            form_class=PasswordResetConfirmForm,
        ),
        name="password_reset_confirmation",
    ),
    # Extending from the initial urls for the success urls redirect/response
    path(
        "password_reset/password_reset_confirmation_email/",
        TemplateView.as_view(template_name="account/user/reset_status.html"),
        name="password_reset_status",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(template_name="account/user/reset_status.html"),
        name="password_reset_complete",
    ),
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path(
        "profile/delete_confirmation/",
        TemplateView.as_view(template_name="account/user/delete_confirmation.html"),
        name="delete_confirmation",
    ),
]
