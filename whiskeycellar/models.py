from django.db import models


class WhiskeyBrand(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Whiskey(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey('WhiskeyBrand', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='whiskey_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
