from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings



class User(AbstractUser):
    pass 


class Case(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy','Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    STATUS_CHOICES =[
        ('open', 'Open'),
        ('solved', 'Solved'),
        ('cold', 'Cold'),

    ]
    title= models.CharField(max_length=255)
    summary=models.TextField()
    status= models.CharField(max_length=20, choices= STATUS_CHOICES, default='cold')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    created_at= models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def __str__(self):
        return self.title
    
class CaseInstance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    lives_remaining = models.IntegerField(default=3)
    status = models.CharField(max_length=20, default='active')  # active, failed, solved

    class Meta:
        unique_together = ('user', 'case')
    def __str__(self):
        return f"{self.user.username} - {self.case.title} ({self.status})"
    
class Clue(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='clues')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Clue {self.order} for {self.case.title}"


# Create your models here.
