from django.db import models
from django.conf import settings


class VisitorLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)

    ip_address = models.GenericIPAddressField()
    page = models.CharField(max_length=500)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=255, blank=True)
    user_agent = models.TextField(blank=True)

    is_logged_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"

    def __str__(self):
        if self.email:
            return f"{self.email} - {self.page}"
        return f"Guest - {self.page}"