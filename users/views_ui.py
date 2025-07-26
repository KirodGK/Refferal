from django.shortcuts import render, redirect
from .models import User
from .utils import generate_auth_code, generate_invite_code

SESSION_KEY = 'logged_user'

def login_view(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        code = generate_auth_code()
        request.session["auth_code"] = code
        request.session["auth_phone"] = phone
        return render(request, "users/login.html", {"code": code})
    return render(request, "users/login.html")

def verify_view(request):
    phone = request.session.get("auth_phone")
    real_code = request.session.get("auth_code")

    if request.method == "POST":
        code = request.POST["code"]
        if code == real_code:
            user, created = User.objects.get_or_create(phone=phone)
            if created:
                user.invite_code = generate_invite_code()
                user.save()
            request.session[SESSION_KEY] = user.phone
            return redirect("ui_profile")
    return render(request, "users/verify.html", {"phone": phone})

def profile_view(request):
    phone = request.session.get(SESSION_KEY)
    if not phone:
        return redirect("ui_login")

    user = User.objects.get(phone=phone)
    referrals = user.referrals.all()

    if request.method == "POST" and not user.referred_by:
        code = request.POST["invite_code"]
        if code != user.invite_code:
            try:
                inviter = User.objects.get(invite_code=code)
                user.referred_by = inviter
                user.save()
            except User.DoesNotExist:
                pass

    return render(request, "users/profile.html", {"user": user, "referrals": referrals})
