from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.models import Orders
from orders.views import user_orders
from account.models import UserBase

from .forms import RegistrationForm, UserEditForm
from .token import AccountActivationTokenGenerator

# Views from here.


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Orders.objects.filter(user_id=user_id).filter(billing_status=False)
    return render(request, "account/user/user_orders.html", {"orders": orders})


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/user/dashboard.html", {"orders": orders})


@login_required
def edit_profile(request):
    if request.method == "POST":
        edit_form = UserEditForm(instance=request.user, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
    else:
        edit_form = UserEditForm(instance=request.user)
    return render(request, "account/user/edit_profile.html", {"edit_form": edit_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


def register(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate you Account"
            message = render_to_string(
                "account/registration/acc_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": AccountActivationTokenGenerator().make_token(user),
                },
            )
            user.email_to_user(subject=subject, message=message)
            return HttpResponse("registered successfully and activation sent")
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and AccountActivationTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return redirect("account/registration/failed_activation.html")
