from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator

# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0) 
    description = models.CharField(max_length=50,default='',null=True,blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1) 

    
    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=False)
    phone = models.CharField(max_length=10,validators = (MinLengthValidator(10),MaxLengthValidator(10))) 
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.first_name} {self.email}"

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def email_exist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    
   
