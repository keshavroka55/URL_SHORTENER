from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def __str__(self):
        return self.short_key
