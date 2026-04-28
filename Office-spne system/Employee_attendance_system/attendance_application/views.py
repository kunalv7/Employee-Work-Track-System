from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import AttendanceRecord
from django.http import JsonResponse
import json


@login_required
def attendance_home(request):

    today = timezone.now().date()

    records_today = AttendanceRecord.objects.filter(
        user=request.user,
        timestamp__date=today
    ).order_by("timestamp")

    total_records = records_today.count()

    clock_in_done = False
    clock_out_done = False

    if total_records >= 1:
        clock_in_done = True

    if total_records >= 2:
        clock_out_done = True

    context = {
        "clock_in_done": clock_in_done,
        "clock_out_done": clock_out_done
    }

    return render(
        request,
        'attendance_application/attendance_home.html',
        context
    )


@login_required
def clock_in_attendance(request):

    if request.method == "POST":

        today = timezone.now().date()

        records_today = AttendanceRecord.objects.filter(
            user=request.user,
            timestamp__date=today
        )

        if records_today.count() >= 1:
            return JsonResponse({
                'error': 'You already clocked in today'
            })

        data = json.loads(request.body)

        if not data.get('photo'):
            return JsonResponse({
                'error': 'Capture Photo is required for clock in'
            })

        record = AttendanceRecord(
            user=request.user,
            remark=data.get('remark'),
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            fence=data.get('fence')
        )

        record.save_base64_image(data['photo'])
        record.save()

        return JsonResponse({'status': 'list_attendance'})

    return render(
        request,
        'attendance_application/clock_in_attendance.html'
    )


@login_required
def clock_out_attendance(request):

    if request.method == "POST":

        today = timezone.now().date()

        records_today = AttendanceRecord.objects.filter(
            user=request.user,
            timestamp__date=today
        )

        if records_today.count() == 0:
            return JsonResponse({
                'error': 'Please clock in first'
            })

        if records_today.count() >= 2:
            return JsonResponse({
                'error': 'You already clocked out today'
            })

        data = json.loads(request.body)

        if not data.get('photo'):
            return JsonResponse({
                'error': 'Capture Photo is required for clock out'
            })

        record = AttendanceRecord(
            user=request.user,
            remark=data.get('remark'),
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            fence=data.get('fence')
        )

        record.save_base64_image(data['photo'])
        record.save()

        return JsonResponse({'status': 'list_attendance'})

    return render(
        request,
        'attendance_application/clock_out_attendance.html'
    )


@login_required
def list_attendance(request):

    today = timezone.now().date()

    archive = request.GET.get("archive")
    month = request.GET.get("month")
    year = request.GET.get("year")

    # Default → aaj ka attendance show
    records = AttendanceRecord.objects.filter(
        user=request.user,
        timestamp__date=today
    ).order_by("timestamp")

    # Archive tick hone par
    if archive == "on" and month and year:

        records = AttendanceRecord.objects.filter(
            user=request.user,
            timestamp__year=year,
            timestamp__month=month
        ).exclude(
            timestamp__date=today
        ).order_by("timestamp")

    # Archive untick + submit → data blank
    if "month" in request.GET and archive != "on":
        records = []

    return render(
        request,
        'attendance_application/list_attendance.html',
        {
            'records': records
        }
    )