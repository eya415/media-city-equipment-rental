#type:ignore
from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True)

    def _str_(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)

    def _str_(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def _str_(self):
        return self.name
    

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries

    def _str_(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivery = models.BooleanField(default=False)
    delivery_name = models.CharField(max_length=100, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

    def _str_(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.product.name} x {self.quantity}"
    






class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    profile_link = models.URLField(blank=True)
    hear_about = models.CharField(max_length=50, blank=True)
    governorate = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    building = models.CharField(max_length=50, blank=True)
    floor = models.CharField(max_length=10, blank=True)
    apartment = models.CharField(max_length=10, blank=True)


    class Meta:
        abstract = True


class IndividualProfile(BaseProfile):
    full_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    professional_category = models.CharField(max_length=50, blank=True)
    portfolio_link = models.URLField(blank=True)
    id_front = models.FileField(upload_to='ids/individual/', blank=True, null=True)
    id_rear = models.FileField(upload_to='ids/individual/', blank=True, null=True)
    other_id = models.FileField(upload_to='ids/individual/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def _str_(self):
        return self.user.username


class CorporateProfile(BaseProfile):
    company_name = models.CharField(max_length=100, blank=True)
    company_address = models.TextField(blank=True)
    company_website = models.URLField(blank=True)
    company_social = models.URLField(blank=True)
    ceo_name = models.CharField(max_length=100, blank=True)
    ceo_phone = models.CharField(max_length=20, blank=True)
    ceo_email = models.EmailField(blank=True)
    ceo_id_front = models.FileField(upload_to='ids/corporate/', blank=True, null=True)
    ceo_id_rear = models.FileField(upload_to='ids/corporate/', blank=True, null=True)
    authorized_name = models.CharField(max_length=100, blank=True)
    authorized_phone = models.CharField(max_length=20, blank=True)
    authorized_email = models.EmailField(blank=True)
    authorized_id_front = models.FileField(upload_to='ids/corporate/', blank=True, null=True)
    authorized_id_rear = models.FileField(upload_to='ids/corporate/', blank=True, null=True)
    tax_certificate = models.FileField(upload_to='docs/corporate/', blank=True, null=True)
    commercial_registration = models.FileField(upload_to='docs/corporate/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def _str_(self):
        return self.user.username


class StudioProfile(BaseProfile):
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(default="temp@example.com", blank=True)
    studio_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def _str_(self):
        return self.user.username