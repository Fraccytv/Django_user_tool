from django.shortcuts import render
from .models import Log

def login_log_list(request):
    logs = Log.objects.all().order_by("-timestamp")[:100]
    return render(request, "logs/login_log_list.html", {"logs": logs})
