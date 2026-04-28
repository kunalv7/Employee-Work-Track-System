from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SwipeApplicationForm
from .models import SwipeApplication

# 🏠 Home
@login_required
def swipe_home(request):
    return render(request, 'swipe_application/swipe_home.html')


# ✅ APPLY SWIPE
@login_required
def swipe_apply(request):
    form = SwipeApplicationForm()

    if request.method == 'POST':
        form = SwipeApplicationForm(request.POST)
        if form.is_valid():
            swipe = form.save(commit=False)
            swipe.user = request.user

            # Assign manager (replace with your logic)
            swipe.manager = User.objects.filter(username='manager1').first()

            swipe.save()
            messages.success(request, "Swipe request applied successfully")
            return redirect('view_swipe_details')

    return render(request, 'swipe_application/swipe_apply.html', {
        'form': form
    })


# ✅ VIEW ALL DETAILS (with card counts)
@login_required
def view_swipe_details(request):
    # User ke saare requests
    user_requests = SwipeApplication.objects.filter(
        user=request.user
    ).order_by('-applied_at')

    # 🔥 Counts for dashboard cards
    total_swipes = user_requests.count()
    approved_count = user_requests.filter(status='approved').count()
    rejected_count = user_requests.filter(status='rejected').count()
    pending_count = user_requests.filter(status='pending').count()

    return render(request, 'swipe_application/view_swipe_details.html', {
        'requests': user_requests,
        'total_swipes': total_swipes,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
    })


# ✅ PENDING SWIPES
@login_required
def recent_swipe(request):
    applications = SwipeApplication.objects.filter(
        user=request.user, status='pending'
    )
    return render(request, 'swipe_application/recent_swipe.html', {
        'applications': applications
    })


# ✅ APPROVED SWIPES
@login_required
def approve_swipe(request):
    applications = SwipeApplication.objects.filter(
        user=request.user, status='approved'
    )
    return render(request, 'swipe_application/approve_swipe.html', {
        'applications': applications
    })


# ✅ REJECTED SWIPES
@login_required
def reject_swipe(request):
    applications = SwipeApplication.objects.filter(
        user=request.user, status='rejected'
    )
    return render(request, 'swipe_application/reject_swipe.html', {
        'applications': applications
    })


# ✅ LAPSED SWIPES
@login_required
def lapsed_swipe(request):
    return render(request, 'swipe_application/lapsed_swipe.html')


