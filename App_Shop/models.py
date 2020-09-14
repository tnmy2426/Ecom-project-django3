from django.db import models


# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=50)
    category_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_title
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    product_name = models.CharField(max_length=264)
    product_image = models.ImageField(upload_to='Products')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    product_preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    product_detail_text = models.TextField(max_length=1000, verbose_name='Description')
    product_price = models.FloatField()
    product_old_price = models.FloatField(default=0.00)
    product_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-product_created_date',]
    
    @staticmethod
    def get_products_by_categoryId(category_id):
        if category_id:
            return Product.objects.filter(product_category=category_id)
        else:
            return Product.objects.all()