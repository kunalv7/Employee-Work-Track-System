from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import UserProfile


# ================= LOGIN =================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_staff:
                return render(request, "authentication/user_login.html", {
                    "error": "Managers must login from Manager Login Page"
                })

            login(request, user)
            return redirect("home")

        return render(request, "authentication/user_login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "authentication/user_login.html")


# ================= HOME =================
@login_required
def home(request):
    return render(request, "authentication/home.html")


# ================= ID CARD =================
@login_required
def id_card(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, "authentication/id_card.html", {
        "profile": profile
    })


# ================= PROFILE =================
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    success = None

    if request.method == "POST":

        # ========= USER TABLE =========
        request.user.first_name = (request.POST.get("first_name") or "").strip()
        request.user.last_name = (request.POST.get("last_name") or "").strip()
        request.user.email = (request.POST.get("email") or "").strip()
        request.user.save()

        # ========= PROFILE FIELDS =========
        fields = [
            "phone", "alternate_phone", "address", "city", "state", "country", "pincode",
            "gender", "marital_status", "blood_group", "nationality",
            "department", "designation", "shift", "manager_name", "work_location",
            "qualification", "college_name", "passing_year",
            "aadhaar_number", "pan_number",
            "emergency_contact_name", "emergency_contact_phone", "emergency_relation",
            "linkedin", "instagram", "bio", "skills", "hobbies"
        ]

        for field in fields:
            value = request.POST.get(field)

            # ✅ Model ke according None ya value set karo
            if value and value.strip():
                setattr(profile, field, value.strip())
            else:
                setattr(profile, field, None)

        # ========= DATE FIELDS =========
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                return None

        profile.dob = parse_date(request.POST.get("dob"))
        profile.joining_date = parse_date(request.POST.get("joining_date"))

        # ========= SALARY (DecimalField) =========
        salary = request.POST.get("salary")
        if salary:
            try:
                profile.salary = float(salary)
            except:
                profile.salary = None
        else:
            profile.salary = None

        # ========= IMAGE DELETE =========
        if request.POST.get("delete_image"):
            if profile.profile_image:
                profile.profile_image.delete(save=False)
                profile.profile_image = None

        # ========= IMAGE UPLOAD =========
        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        # ========= SAVE =========
        profile.save()

        success = "Profile Updated Successfully"

    return render(request, "authentication/profile.html", {
        "profile": profile,
        "success": success
    })


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("user_login")

@login_required
def id_card(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, "authentication/id_card.html", {
        "profile": profile
    })