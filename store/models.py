from django.db import models

# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0) 
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/products/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1) 

    
    def __str__(self):
        return self.name