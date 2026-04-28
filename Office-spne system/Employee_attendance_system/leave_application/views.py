from django.shortcuts import render, redirect, get_object_or_404
from .forms import LeaveApplicationForm
from django.contrib.auth.decorators import login_required
from .models import LeaveApplication
from django.contrib.auth.models import User

# 🏠 HOME
def leave_home(request):
    return render(request, 'leave_application/leave_home.html')


# ✅ APPLY
@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user

            # 👇 Manager assign (change logic if needed)
            leave.manager = User.objects.filter(username='manager1').first()

            leave.save()
            return redirect('leave_home')
    else:
        form = LeaveApplicationForm()

    return render(request, 'leave_application/leave_apply.html', {'form': form})


# ✅ USER SIDE

# Pending
@login_required
def recent_leave(request):
    applications = LeaveApplication.objects.filter(
        user=request.user,
        status='pending'
    ).order_by('-applied_at')

    return render(request, 'leave_application/recent_leave.html', {'applications': applications})


# Approved
@login_required
def approve_leave(request):
    applications = LeaveApplication.objects.filter(
        user=request.user,
        status='approved'
    ).order_by('-applied_at')

    return render(request, 'leave_application/approve_leave.html', {'applications': applications})


# Rejected
@login_required
def reject_leave(request):
    applications = LeaveApplication.objects.filter(
        user=request.user,
        status='rejected'
    ).order_by('-applied_at')

    return render(request, 'leave_application/reject_leave.html', {'applications': applications})


# 🧠 MANAGER SIDE

# All pending requests for manager
@login_required
def manager_leave_requests(request):
    applications = LeaveApplication.objects.filter(
        manager=request.user,
        status='pending'
    )

    return render(request, 'leave_application/manager_requests.html', {'applications': applications})


# Approve
@login_required
def approve_leave_request(request, id):
    leave = get_object_or_404(LeaveApplication, id=id)

    if request.user == leave.manager:
        leave.status = 'approved'
        leave.save()

    return redirect('manager_leave_requests')


# Reject
@login_required
def reject_leave_request(request, id):
    leave = get_object_or_404(LeaveApplication, id=id)

    if request.user == leave.manager:
        leave.status = 'rejected'
        leave.save()

    return redirect('manager_leave_requests')


# Lapsed
def lapsed_leave(request):
    return render(request, 'leave_application/lapsed_leave.html')

# ===========================
# 📋 USER LEAVE LIST (CANCEL PAGE)
# ===========================
@login_required
def my_leave_requests(request):

    leaves = LeaveApplication.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    return render(request, "leave_application/my_leave_requests.html", {
        "leaves": leaves
    })


# ===========================
# ❌ CANCEL LEAVE
# ===========================
@login_required
def cancel_leave(request, id):

    leave = get_object_or_404(LeaveApplication, id=id, user=request.user)

    # ✅ Only pending leave can be cancelled
    if leave.status == "pending":
        leave.status = "cancelled"
        leave.save()

    return redirect("my_leave_requests")