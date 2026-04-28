from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import time

from attendance_application.models import AttendanceRecord
from leave_application.models import LeaveApplication


@login_required
def quick_info_home(request):

    user = request.user
    today = timezone.now().date()

    # ================= PROFILE =================
    full_name = f"{user.first_name} {user.last_name}".strip()
    email = user.email

    # ================= LEAVE =================
    TOTAL_LEAVES = 20

    approved_leaves = LeaveApplication.objects.filter(
        user=user,
        status__iexact="approved"
    )

    used_leaves = sum(
        (leave.to_date - leave.from_date).days + 1
        for leave in approved_leaves
    )

    leave_balance = TOTAL_LEAVES - used_leaves
    if leave_balance < 0:
        leave_balance = 0

    leave_used_percent = (used_leaves / TOTAL_LEAVES) * 100 if TOTAL_LEAVES else 0

    # ================= ATTENDANCE =================
    today_records = list(
        AttendanceRecord.objects.filter(
            user=user,
            timestamp__date=today
        ).order_by("timestamp")
    )

    record_count = len(today_records)

    today_status = "Absent"
    today_hours = "0h 00m"
    in_time_display = "--"
    out_time_display = "--"

    if record_count >= 1:
        in_time_display = timezone.localtime(
            today_records[0].timestamp
        ).strftime("%I:%M %p")

    if record_count >= 2:
        out_time_display = timezone.localtime(
            today_records[1].timestamp
        ).strftime("%I:%M %p")

        diff = today_records[1].timestamp - today_records[0].timestamp
        total_seconds = int(diff.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        today_hours = f"{hours}h {minutes:02d}m"

        if hours >= 9:
            today_status = "Present"
        elif hours >= 4:
            today_status = "Half Day"
        else:
            today_status = "Absent"

    elif record_count == 1:
        today_status = "Incomplete"

    # ================= LATE COUNT =================
    late_count = AttendanceRecord.objects.filter(
        user=user,
        timestamp__date__month=today.month,
        timestamp__time__gt=time(10, 0)
    ).values("timestamp__date").distinct().count()

    # ================= HOLIDAY LIST (FULL YEAR) =================
    holidays = [
        ("Republic Day", "26 Jan 2026"),
        ("Holi", "March 2026"),
        ("Good Friday", "April 2026"),
        ("Labour Day", "1 May 2026"),
        ("Independence Day", "15 Aug 2026"),
        ("Gandhi Jayanti", "2 Oct 2026"),
        ("Diwali", "Nov 2026"),
        ("Christmas", "25 Dec 2026"),
    ]

    # ================= CONTEXT =================
    context = {
        "full_name": full_name,
        "email": email,

        # Leave
        "total_leaves": TOTAL_LEAVES,
        "used_leaves": used_leaves,
        "leave_balance": leave_balance,
        "leave_used_percent": leave_used_percent,

        # Attendance
        "today_status": today_status,
        "today_hours": today_hours,
        "in_time": in_time_display,
        "out_time": out_time_display,

        # Extras
        "late_count": late_count,
        "holidays": holidays,
    }

    return render(request, "quick_info.html", context)