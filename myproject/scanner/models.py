from django.db import models

# Create your models here.
# models.py

class HallOfFame(models.Model):
    url = models.URLField(max_length=200)
    grade = models.CharField(max_length=2)  # Only A or A+

    def __str__(self):
        return f"{self.url} - {self.grade}"

class HallOfShame(models.Model):
    url = models.URLField(unique=True)
    grade = models.CharField(max_length=2)  # Only F

    def __str__(self):
        return f"{self.url} - {self.grade}"
class RecentScan(models.Model):
    url = models.URLField()
    grade = models.CharField(max_length=2)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.grade} - {self.scanned_at}"

class GradeSummary(models.Model):
    grade = models.CharField(max_length=5)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.grade} - {self.count}"
