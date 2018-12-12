from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1 , choices=( ('M' , 'Male'),('F' , 'Female') ),null=True )
    phone_regex = RegexValidator(regex=r'^[1-9]\d{9}$', message="enter a valid phone number")
    phone_number = models.CharField(validators=[phone_regex],max_length=10, blank=True)
    profile_pic = models.ImageField(default='prof1.jpg', upload_to="profile_pics", null=True, blank=True)

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender = User)
    # def create_profile(sender,instance,created, **kwargs):
    #
    #     if created:
    #         Userprofile.objects.create(user = instance)
    #     instance.userprofile.save()
