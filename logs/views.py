# logs/views.py (opdateret)
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from utils.decorators import session_login_required
from .models import Log
from .forms import LogFilterForm

@session_login_required
def login_log_list(request):
    qs = Log.objects.select_related("user").all()

    form = LogFilterForm(request.GET or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        ip = form.cleaned_data.get("ip")
        status = form.cleaned_data.get("status")
        event_type = form.cleaned_data.get("event_type")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")

        if username:
            qs = qs.filter(user__username__icontains=username)
        if ip:
            qs = qs.filter(ip_address=ip)
        if status:
            qs = qs.filter(status=status)
        if event_type:
            qs = qs.filter(event_type=event_type)
        if date_from:
            qs = qs.filter(timestamp__date__gte=date_from)
        if date_to:
            qs = qs.filter(timestamp__date__lte=date_to)

    paginator = Paginator(qs, 50)
    page = request.GET.get("page")
    logs = paginator.get_page(page)

    # bevar query params i template
    qp = request.GET.copy()
    if "page" in qp:
        qp.pop("page")
    return render(request, "logs/login_log_list.html", {"logs": logs, "form": form, "query": qp.urlencode()})