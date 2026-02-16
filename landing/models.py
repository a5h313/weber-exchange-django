from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Condition(models.TextChoices):
    NEW = 'new', 'New'
    EXCELLENT = 'excellent', 'Excellent'
    GOOD = 'good', 'Good'
    FAIR = 'fair', 'Fair'
    POOR = 'poor', 'Poor'

class Location(models.TextChoices):
    SU = 'shepherd-union', 'Shepherd Union'
    LI = 'steward-library', 'Steward Library'
    NB = 'noorda-building', 'Noorda Building'
    TY = 'tracy-hall', 'Tracy Hall'


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=50)
    condition = models.CharField(
        max_length=10,
        choices=Condition.choices,
        default=Condition.GOOD,
    )
    location = models.CharField(
        max_length=20,
        choices=Location.choices,
        default=Location.SU,
    )
    available = models.BooleanField(default=True)
    postedAt = models.DateTimeField(auto_now_add=True)
    seller = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(default='', null=False)

    def __str__(self):
        return f"{self.title} | ${self.price}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)




