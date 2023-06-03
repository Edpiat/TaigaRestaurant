from django.db import models

#Importing the USER model that is built in the django at contrib.auth and contains info about users
from django.contrib.auth.models import User

#Creating a model for the category after which comes the fields with formats and params, ID fields is set by default so no need to specify it
class Category(models.Model):
    slug = models.SlugField()

    #The func below lets us see the title of an item at API instead just number of the object
    def __str__(self):
        return self.title
    #The max_length defines max allowed characters for that field, db_index =TRUE sets an index for a column to easily search and filter records
    title = models.CharField(max_length=255, db_index=True)

#Creating a model for the Menuitem after which comes the fields with formats and params, ID fields is set by default so no need to specify it
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

#Creating a model for the Cart after which comes the fields with formats and params, ID fields is set by default so no need to specify it
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('menuitem', 'user')

#Creating a model for the Order after which comes the fields with formats and params, ID fields is set by default so no need to specify it
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date = models.DateField(db_index=True)

#Creating a model for the OrderItem after which comes the fields with formats and params, ID fields is set by default so no need to specify it
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')