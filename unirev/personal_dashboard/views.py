

from django.shortcuts import render


def personal_dashboard(request):
    return render(request, "personal_dashboard/base.html")