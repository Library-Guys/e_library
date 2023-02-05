from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_image')
    city = models.CharField(max_length=50, blank=True)
    zone = models.CharField(max_length=50, blank=True)
    contact_no = models.CharField(max_length=12, blank=True)
    tole = models.CharField(max_length=50, blank=True)
    bio = models.TextField()

    def get_absolute_url(self):
        return reverse("auth_users:profile", args=[self.slug])

    def __str__(self):
        return self.user.username
    
    # def save(self):
    #     super().save()

    #     img = Image.open(self.avatar.path)

    #     if img.height > 10 or img.width > 10:
    #         new_img = (50, 50)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)