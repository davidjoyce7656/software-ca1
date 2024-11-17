from django.db import models

# Create your models here.
class WhiskeyBrand(models.Model):
    brand_name = models.CharField(max_length=200)
    proof = models.IntegerField(default=0)
    country_origin = models.CharField(max_length=200)
    
    def __str__(self):
        return self.brand_name