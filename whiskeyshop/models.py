from django.db import models

# Create your models here.
class WhiskeyBrand(models.Model):
    brand_name = models.CharField(max_length=200)
    proof = models.IntegerField(default=0)
    country_origin = models.CharField(max_length=200)
    
    def __str__(self):
        return self.brand_name


class Whiskey(models.Model):
    name = models.CharField(max_length=200)  # Name of the whiskey
    description = models.TextField()         # Description of the whiskey
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the whiskey
    image = models.ImageField(upload_to='whiskeys/')  # Image of the whiskey (requires MEDIA_ROOT setup)

    def __str__(self):
        return self.name