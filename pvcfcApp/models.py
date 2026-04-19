from django.db import models
from django.contrib.auth.models import User

# ================= CATEGORY =================
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


# ================= CUSTOMER =================
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


# ================= PRODUCT =================
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    # ảnh chính
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    # thêm info riêng cho phân bón
    brand = models.CharField(max_length=200, null=True, blank=True)  # ví dụ: Cà Mau
    weight = models.CharField(max_length=50, null=True, blank=True)  # 50kg, 25kg
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''


# ================= MULTI IMAGE (GIỐNG SHOPEE) =================
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.product.name
    



# ================= ORDER =================
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    payment_method = models.CharField(max_length=20, choices=[
    ('cod', 'Cash on Delivery'),
    ('vnpay', 'VNPay'),
    ], default='cod')

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        return sum([item.get_total for item in items])

    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        return sum([item.quantity for item in items])


# ================= ORDER ITEM =================
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        return self.product.price * self.quantity


# ================= SHIPPING =================
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.address