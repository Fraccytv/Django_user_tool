from urllib.parse import urlparse
from django.urls import reverse, NoReverseMatch

def get_safe_next_url(request) -> str:
    """
    Returnér en sikker redirect-URL baseret på ?next=.
    Tillader KUN interne redirects (relative stier eller samme host).
    Fallback-rækkefølge: 'home' -> 'login' -> '/'.
    """
    nxt = request.GET.get("next")

    if nxt:
        # 1) Tillad kun rene relative stier (ikke '//' som kan være ekstern protokol-relativ)
        if nxt.startswith("/") and not nxt.startswith("//"):
            return nxt

        # 2) Hvis absolut URL: accepter kun samme host og korrekt skema
        parsed = urlparse(nxt)
        if parsed.netloc and parsed.netloc == request.get_host():
            allowed_schemes = ["https"] if request.is_secure() else ["http", "https"]
            if parsed.scheme in allowed_schemes:
                return nxt

    # 3) Fallback: 'home' -> 'login' -> '/'
    for name in ("home", "login"):
        try:
            return reverse(name)
        except NoReverseMatch:
            continue
    return "/"
