from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    # Custom user manager for creating users and superusers
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise ValueError('The Password field must be set')
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
    
    
# Custom user model that extends AbstractUser
# This allows us to use email as the username field and add additional fields
class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email


# User profile model that extends the CustomUser model
# This allows us to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.email
    

def default_list():
    return []

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Bluetooth Speakers", "Bluetooth Speakers"),
        ("Headphones", "Headphones"),
        ("Wireless Earbuds", "Wireless Earbuds"),
        ("Smartwatches", "Smartwatches"),
        ("Screen Protectors", "Screen Protectors"),
        ("Phone Cases", "Phone Cases"),
        ("Chargers & Cables", "Chargers & Cables"),
        ("Power Banks", "Power Banks"),
        ("Accessories", "Accessories"),
        ("Wearables", "Wearables"),
        ("Budget Phones", "Budget Phones"),
        ("Flagship Phones", "Flagship Phones"),
        ("Gaming Phones", "Gaming Phones"),
        ("Tablets", "Tablets"),
    ]
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    storage = models.JSONField(default=default_list, blank=True, null=True)
    colors = models.JSONField(default=default_list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.user.username}'s cart"
    
    # Get all cart items related to the user through the cart
    def get_items(self):
        return self.items.all()

    # Get the total price of the cart
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.get_items())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.cart.user.username}'s cartitem ({self.quantity} {self.product.name})"
    
    # Get the total price of cart items
    def get_total_price(self):
        return self.quantity * self.product.price


# In a real-world application, i would use a more secure way for managing payment details
class CardDetails(models.Model):
    card_number = models.CharField(max_length=19) 
    expiry = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.TextField()
    billing_address = models.TextField()
    payment_method = models.CharField(max_length=50, choices=[('card', 'Credit/Debit Card'), ('paypal', 'PayPal')])
    card = models.OneToOneField(CardDetails, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, default='Order placed')
    placed_at = models.DateTimeField(auto_now_add=True)
    
     # Get all order items related to the user through the order
    def get_items(self):
        return self.items.all()
    
    # Get the total price of the order
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.get_items())
    
    # def __str__(self):
    #     return str(self.id)


# This model represents an item in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Order placed')
    quantity = models.PositiveIntegerField()
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    
    def get_total_price(self):
        return self.quantity * self.product.price


