from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255,blank=True)
    text = models.TextField()
    duration = models.FloatField(validators=[MinValueValidator(limit_value = 1.0)])
    resolution = models.CharField(max_length=10)
    background_color = models.CharField(max_length=7)
    font_color = models.CharField(max_length=7)
    font_scale = models.FloatField(default=2.0,validators=[MinValueValidator(limit_value = 1.0)])
    thickness = models.IntegerField(default=3,validators=[MinValueValidator(limit_value = 1)])
    include_stripe = models.BooleanField(default=False)
    stripe_color = models.CharField(max_length=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
