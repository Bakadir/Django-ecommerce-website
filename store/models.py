from django.db import models
from django.utils.text import slugify
# Create your models here.

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User

def validate_league_choices(value):
    if len(value) != 2:
        raise ValidationError('You must select exactly two leagues.')
def upload_logo(instance, filename):
        return f"static/images/{instance.league}/{instance.name}.jpg"
class Club(models.Model):
    LEAGUE_CHOICES = [
        ('Bundesliga', 'Bundesliga'),
        ('Champions League', 'Champions League'),
        ('Europa League', 'Europa League'),
        ('La Liga', 'La Liga'),
        ('Ligue 1', 'Ligue 1'),
        ('Premier League', 'Premier League'),
        ('Serie A', 'Serie A'),
        ('World Cup', 'World Cup'),
        ('Worldwide Jerseys', 'Worldwide Jerseys'),
        ('B-Jerseys Specials', 'B-Jerseys Specials'),
        
    ]

    name = models.CharField(max_length=100)
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES)
    image = models.ImageField(upload_to=upload_logo, blank=True, null=True, max_length=200)
    
    def __str__(self):
        return f"{self.name} - {self.league}"
    def logoURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    

def upload_extra_photos2(instance, filename):
        return f"static/images/{instance.club.league}/{instance.club.name}/extra_photos2.jpg"
def upload_extra_photos3(instance, filename):
        return f"static/images/{instance.club.league}/{instance.club.name}/extra_photos3.jpg"
def upload_extra_photos4(instance, filename):
        return f"static/images/{instance.club.league}/{instance.club.name}/extra_photos4.jpg"
def upload_photo(instance, filename):
        return f"static/images/{instance.club.league}/{instance.club.name}/photo1.jpg"
def upload_extra_photos1(instance, filename):
        return f"static/images/{instance.club.league}/{instance.club.name}/extra_photos1.jpg"
class Product(models.Model):

    SEASON_CHOICES = [
    ('2023-24', '2023-24'),
    ('2023', '2023'),
    ('2022-23', '2022-23'),
    ('2022', '2022'),
    ('2021-22', '2021-22'),
    ('2021', '2021'),
    ('2020-21', '2020-21'),
    ('2020', '2020'),
    ('2019-20', '2019-20'),
    ('2019', '2019'),
    ('2018-19', '2018-19'),
    ('2018', '2018'),
    ('2017-18', '2017-18'),
    ('2017', '2017'),
    ('2016-17', '2016-17'),
    ('2016', '2016'),
    ('2015-16', '2015-16'),
    ('2015', '2015'),
    ('2014-15', '2014-15'),
    ('2014', '2014'),
    ('2013-14', '2013-14'),
    ('2013', '2013'),
    ('2012-13', '2012-13'),
    ('2012', '2012'),
    ('2011-12', '2011-12'),
    ('2011', '2011'),
    ('2010-11', '2010-11'),
    ('2010', '2010'),
    ('2008-09', '2008-09'),
]


    TYPE_CHOICES = [
        ('home', 'home'),
        ('away', 'away'),
        ('third', 'third'),
        ('Special Edition', 'Special Edition'),
        ('Special Edition 2', 'Special Edition 2'),
        ('Special Edition 3', 'Special Edition 3'),
        ('Special Edition 4', 'Special Edition 4'),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    season = models.CharField(max_length=100, choices=SEASON_CHOICES)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to=upload_photo,null=True, blank=True, max_length=200)
    extra_photos = models.ImageField(upload_to=upload_extra_photos1, blank=True, null=True, max_length=200)
    extra_photos2 = models.ImageField(upload_to=upload_extra_photos2, blank=True, null=True, max_length=200)
    extra_photos3 = models.ImageField(upload_to=upload_extra_photos3, blank=True, null=True, max_length=200)
    extra_photos4 = models.ImageField(upload_to=upload_extra_photos4, blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.club.league} - {self.club.name} - {self.season} - {self.type} "
    
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    def get_absolute_url(self):
        club_slug = slugify(self.club.name)
        return reverse('store:product_detail', args=[club_slug, self.season, self.type])
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.CharField(max_length=100, null=True)
    complete = models.BooleanField(default=False)

    firstname= models.CharField(max_length=200, null=False, blank=True)
    lastname = models.CharField(max_length=200, null=False, blank=True)
    email =  models.EmailField(max_length=500, null=False, blank=True)
    phone_number = models.CharField(max_length=200, null=False, blank=True)

    country = models.CharField(max_length=200, null=False, blank=True)
    city = models.CharField(max_length=200, null=False, blank=True)
    zipcode = models.CharField(max_length=200, null=False, blank=True)
    address = models.CharField(max_length=200, null=False, blank=True)


    def __str__(self):
        return f"{self.user} -{self.complete}- {self.country} - {self.city} "

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([1 for item in orderitems])
        return total 
class OrderItem(models.Model):
    SIZE_CHOICES = [
		('XS', 'XS'),
		('S', 'S'),
		('M', 'M'),
		('L', 'L'),
		('XL', 'XL'),
		]
    
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    size = models.CharField(max_length=10,choices=SIZE_CHOICES)

    def __str__(self):
            
        return f"{self.order} - {self.product.club.name} - {self.product.season} - {self.product.type} - {self.size} - {self.quantity}  "
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



	