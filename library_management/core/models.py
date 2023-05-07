from django.db import models

# Create your models here.
class LibraryUsers(models.Model):
    username = models.CharField(max_length=20, verbose_name="username", help_text="username")
    password = models.CharField(max_length=20, verbose_name="password", help_text="password",)
    user_type = models.CharField(max_length=20, verbose_name="user_type", help_text="user_type",)



class Books(models.Model):
    status_choices = [
        ("BORROWED", "book_unavailable"),
        ("AVAILABLE", "book_available"),
    ]
    book_title = models.CharField(max_length=200, verbose_name="username", help_text="username")
    book_status = models.CharField(max_length=200, choices=status_choices,default = 'AVAILABLE')
    user = models.ForeignKey(LibraryUsers, on_delete=models.PROTECT,null=True,default=None)
   