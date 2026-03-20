from django.db import models
from django.utils import timezone

class OutbreakReport(models.Model):
    source = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    text = models.TextField()
    detected_disease = models.CharField(max_length=100)
    probability = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    predicted_label = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.detected_disease} in {self.location} from {self.source}"