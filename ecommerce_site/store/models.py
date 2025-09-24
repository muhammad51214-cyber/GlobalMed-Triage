from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    """Product categories for better organization"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:category', args=[self.slug])


class Product(models.Model):
    """Product model with all essential e-commerce fields"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, help_text="URL to product image")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['available', 'created_at']),
            models.Index(fields=['category', 'available']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def get_image_url(self):
        """Return image URL or placeholder"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/img/placeholder.jpg'


class CartItem(models.Model):
    """Cart items for both logged-in users and session-based carts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['user', 'product'],
            ['session_id', 'product'],
        ]
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name} ({self.quantity})"
        return f"Session {self.session_id} - {self.product.name} ({self.quantity})"
    
    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    """Order model to track customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Shipping information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('store:order_detail', args=[self.order_id])


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.order_id} - {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.unit_price
