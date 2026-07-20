from .models import VisitorLog
import requests

class VisitorLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Static, media aur admin static ko skip karo
        if (
            request.path.startswith("/static/")
            or request.path.startswith("/media/")
        ):
            return response

        ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT", "")

        browser = "Unknown"

        if "Chrome" in user_agent:
            browser = "Chrome"
        elif "Firefox" in user_agent:
            browser = "Firefox"
        elif "Edg" in user_agent:
            browser = "Edge"
        elif "Safari" in user_agent:
            browser = "Safari"

        if request.user.is_authenticated:
            username = request.user.username
            email = request.user.email
            user = request.user
            logged_in = True
        else:
            username = "Guest"
            email = "Guest"
            user = None
            logged_in = False
            
            
        country = ""
        city = ""


        try:
            geo_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
            data = geo_response.json()

            if data.get("status") == "success":
                country = data.get("country", "")
                city = data.get("city", "")
        except Exception:
            pass
        
        VisitorLog.objects.create(
            user=user,
            username=username,
            email=email,
            ip_address=ip,
            page=request.path,
            browser=browser,
            user_agent=user_agent,
            is_logged_in=logged_in,
            country=country,
            city=city,
        )

        return response