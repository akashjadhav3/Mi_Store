from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
        product_id = models.AutoField
        product_name = models.CharField(max_length=50)
        category = models.CharField(max_length=50, default="")
        subcategory = models.CharField(max_length=50, default="")
        price = models.IntegerField(default=0)
        desc = models.TextField()
        pub_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
        image = models.ImageField(upload_to='shop/images', default="",blank=True,null=True)
        image1 = models.ImageField(upload_to='shop/images', default="",blank=True,null=True)
        image2 = models.ImageField(upload_to='shop/images', default="",blank=True,null=True)
        image3 = models.ImageField(upload_to='shop/images', default="",blank=True,null=True)
        image4 = models.ImageField(upload_to='shop/images', default="",blank=True,null=True)


        def __str__(self):
            return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Login(models.Model):
    msg_id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=70, default="")
    psw = models.CharField(max_length=70)


    def __str__(self):
        return self.uname

class Signin(models.Model):
    msg_id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=50)
    phone = models.CharField(max_length=70, default="")
    email = models.CharField(max_length=70, default="")
    psw = models.CharField(max_length=70,default="")

    def __str__(self):
        return self.uname

class Orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    order_id2 = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."



class Payments(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE,blank=True,null=True)
    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    signature = models.CharField(max_length=255)
    order_related = models.ForeignKey(Orders,on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


    class Meta:
        ordering = ('-created',)
        verbose_name = 'payment'
        verbose_name_plural = 'payment'