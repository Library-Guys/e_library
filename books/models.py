from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
# Create your models here.

class Genere(models.Model):
    name = models.CharField(max_length=50, db_index = True)
    slug = models.SlugField(max_length = 100,unique=True)
    
    # class Meta:
    #     verbose_name_plural = 'genere'
        
    # def get_absolute_url(self):#for dynamic link for category
    #     return reverse('store:category_list', args=[self.slug])
        
    def __str__(self):
        return self.name
    
class Pdf_Info(models.Model):
    category = models.ForeignKey(Genere,related_name='genere', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=250)
    image = models.ImageField(upload_to = 'book_image/')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    book_pdf = models.FileField(upload_to='book/')
    
    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.slug])
    
    def __str__(self):
        return self.title
<<<<<<< HEAD

#
# class Books(models.Model):
#     Name = models.CharField(max_length=100)
#     Author = models.CharField(max_length=100)
#     Edition = models.CharField(max_length=30)
#     title = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.Name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=10)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user)

class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    # expiry_date = models.DateField(default=expiry)
=======
    
    

    
>>>>>>> demo
