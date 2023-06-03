#Serializers need to pass instructions related to databases from a web app and vice versa

from rest_framework import serializers

#importing a User model which is built in, in django, that's why we do it separate from other models
from django.contrib.auth.models import User

#importing a decimal package for decimals
from decimal import Decimal

#importing models created
from .models import Category, MenuItem, Cart, Order, OrderItem



#Serializer for the category model, we can adjust the fields that are going to be displayed and avalable for the wep app process by specifying them5
# in the meta class, in the "fields"
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    #Below we specify that category table is used to represent the target of the relationship using its primary key and also add there all objects
    #of the category table
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        #We can change the name of the field if we want, for that we remove the one we want from the list below, add there a new name of field
        # After that, above the MEta class we create a variable named after the name we want and assign it
        # =serializers.type_of_field(source='original name of field we changed')
        fields = ['id', 'title', 'price', 'category', 'featured']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        #The default variable below serizlizes only the information for the current user who is authenticated and using the API
        default=serializers.CurrentUserDefault()
    )


    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    #Below represents the edited order field to orderitem which represents order and its dependancies (many=True)
    # and is able only for GET request (read_only=True)
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']