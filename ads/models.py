from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('ожидает', 'Ожидает'),
        ('принята', 'Принята'),
        ('отклонена', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ожидает')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver} ({self.status})"
