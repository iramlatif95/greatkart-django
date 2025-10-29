from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True) 
    description=models.TextField(max_length=250,blank=True)
    cat_image=models.ImageField(upload_to='categories',blank=True)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories' # without this the in a admin panel its name is the categorys 's'

    def __str__(self):
        return self.category_name
     
    # custom meghod  Dynamically generate the URL of the product detail page
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    


# Create your models here.
