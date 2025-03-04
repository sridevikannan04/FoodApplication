from django.contrib.auth.models import User
from django.db import models

# Role Table
class Role(models.Model):
    role_name=models.CharField(max_length=20)

    # def __str__(self):
    #     return self.role_name

    class Meta:
        db_table = "adm_role"

# UserRole Table (Links Users & Roles)
class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) # Each user has one role
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user

    class Meta:
        db_table = "UserRole"

class FoodItems(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    price=models.FloatField()
    category=models.CharField(max_length=50)
    image=models.FileField(upload_to='image')
    available=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.CharField()
    updated_by=models.CharField(null=True)
    updated_date = models.DateTimeField(null = True)
    
    # def __str__(self):
    #     return self.name
    
    class Meta:
        db_table = "FoodItems"
    
    
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    food_item=models.ForeignKey(FoodItems,on_delete=models.CASCADE)
    quantity=models.IntegerField() 
    # product= models.ForeignKey(FoodItems,on_delete = models.CASCADE)
    price = models.FloatField(max_length=10)
#    added_at=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.CharField()
    updated_by=models.CharField(null=True)
    updated_date = models.DateTimeField(null = True)
#    def __str__(self):
#        return self.user

    def get_total_price(self):
        return self.quantity * self.food_item.price
   
    class Meta:
        db_table = "Cart"
   

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    status = models.CharField(max_length=50, default="Pending")  
    payment_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.CharField()
    updated_by=models.CharField(null=True)
    updated_date = models.DateTimeField(null = True)

    class Meta:
        db_table = "Order"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.CharField()
    updated_by=models.CharField(null=True)
    updated_date = models.DateTimeField(null = True)
    
    class Meta:
        db_table = "OrderItem"  

class customer(models.Model):
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    dob=models.CharField(max_length=50, null=True)
    gender=models.CharField(max_length=50)
    mobile=models.CharField() 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.CharField()
    updated_by=models.CharField(null=True)
    updated_date = models.DateTimeField(null = True)

    # def __str__(self):
    #     return self.username
    
    class Meta:
        db_table = "customer"