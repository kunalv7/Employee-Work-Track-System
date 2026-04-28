from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance_application.models import AttendanceRecord
from swipe_application.models import SwipeApplication
from leave_application.models import LeaveApplication   # ✅ ADD
from collections import defaultdict
from datetime import time, date, datetime, timedelta
from django.utils import timezone
import calendar

# Public Holiday List
PUBLIC_HOLIDAYS = [
    "2026-01-26",
    "2026-08-15",
    "2026-10-02",
]

@login_required
def my_attendance_home(request):

    today = timezone.now().date()

    current_month = today.month
    current_year = today.year

    month = request.GET.get("month")
    year = request.GET.get("year")

    if not month or not year:
        month = current_month
        year = current_year
    else:
        month = int(month)
        year = int(year)

    archive_flag = request.GET.get("archive") == "1"

    # ================= ATTENDANCE =================
    if archive_flag:
        records = AttendanceRecord.objects.filter(user=request.user).order_by('timestamp')
    else:
        records = AttendanceRecord.objects.filter(
            user=request.user,
            timestamp__month=month,
            timestamp__year=year
        ).order_by('timestamp')

    grouped_records = defaultdict(list)
    for record in records:
        grouped_records[record.timestamp.date()].append(record)

    # ================= SWIPE =================
    if archive_flag:
        swipes = SwipeApplication.objects.filter(user=request.user, status='approved')
    else:
        swipes = SwipeApplication.objects.filter(
            user=request.user,
            status='approved',
            request_date__month=month,
            request_date__year=year
        )

    swipe_map = {s.request_date: s for s in swipes}

    # ================= LEAVE =================
    leaves = LeaveApplication.objects.filter(
        user=request.user,
        status="approved"
    )

    leave_dates = set()
    for leave in leaves:
        current = leave.from_date
        while current <= leave.to_date:
            leave_dates.add(current)
            current += timedelta(days=1)

    # ==========================================

    total_days = calendar.monthrange(year, month)[1] if not archive_flag else today.day

    attendance_data = []
    total_portion = 0
    total_minutes = 0
    total_late = 0

    for day in range(1, total_days + 1):

        current_date = date(year, month, day)
        recs = grouped_records.get(current_date, [])
        recs = sorted(recs, key=lambda x: x.timestamp)

        swipe = swipe_map.get(current_date)

        clock_in = None
        clock_out = None
        is_swipe_in = False
        is_swipe_out = False

        # CLOCK IN
        if len(recs) >= 1:
            clock_in = recs[0]
        elif swipe and swipe.in_time:
            clock_in = swipe
            is_swipe_in = True

        # CLOCK OUT
        if len(recs) >= 2:
            clock_out = recs[1]
        elif swipe and swipe.out_time:
            clock_out = swipe
            is_swipe_out = True

        status = "DA"
        total_hours = "0h 00m"
        late_status = "--"

        # ================= HOLIDAY =================
        if current_date.weekday() == 6:
            status = "WO"
        elif str(current_date) in PUBLIC_HOLIDAYS:
            status = "PH"

        # ================= ✅ LEAVE FIX =================
        if current_date in leave_dates:
            status = "LV"

            # 🔥 REMOVE ATTENDANCE DATA
            clock_in = None
            clock_out = None
            is_swipe_in = False
            is_swipe_out = False
        # =============================================

        # ================= LATE =================
        if clock_in:

            if is_swipe_in and clock_in.in_time:
                check_time = clock_in.in_time
            else:
                local_time = timezone.localtime(clock_in.timestamp)
                check_time = local_time.time()

            if check_time > time(11, 0):
                late_status = "1"

                if not swipe:
                    total_late += 1

        # ================= HOURS =================
        if clock_in and clock_out:

            if is_swipe_in:
                in_time = timezone.make_aware(datetime.combine(current_date, clock_in.in_time))
            else:
                in_time = clock_in.timestamp

            if is_swipe_out:
                out_time = timezone.make_aware(datetime.combine(current_date, clock_out.out_time))
            else:
                out_time = clock_out.timestamp

            diff = out_time - in_time
            total_seconds = int(diff.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            total_hours = f"{hours}h {minutes:02d}m"
            total_minutes += (hours * 60 + minutes)

            if status not in ["WO", "PH", "LV"]:
                if hours >= 9:
                    status = "DP"
                elif hours >= 4:
                    status = "HD"
                else:
                    status = "DA"

        # ================= SINGLE ENTRY =================
        if (clock_in and not clock_out) or (clock_out and not clock_in):
            if status not in ["WO", "PH", "LV"]:
                status = "DA"

        # ================= SWIPE =================
        if swipe and clock_in and clock_out:
            if status not in ["WO", "PH", "LV"]:
                status = "DP"

        attendance_data.append({
            "date": current_date,
            "clock_in": clock_in,
            "clock_out": clock_out,
            "status": status,
            "total_hours": total_hours,
            "late": late_status,
            "is_swipe_in": is_swipe_in,
            "is_swipe_out": is_swipe_out
        })

        total_portion += 1

    total_hours_sum = f"{total_minutes // 60}h {total_minutes % 60:02d}m"

    return render(
        request,
        "my_attendance_application/my_attendance_home.html",
        {
            "records": attendance_data,
            "total_portion": total_portion,
            "total_hours_sum": total_hours_sum,
            "total_late": total_late,
            "selected_month": str(month),
            "selected_year": str(year),
        }
    )