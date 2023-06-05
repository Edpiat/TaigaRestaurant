
#importing generics which help our classes to perform HTTP methods like GET, POST, PUT, PATCH
from rest_framework import generics

#Importing the IsAuthenticated class which allows to check if user is authenticated
from rest_framework.permissions import IsAuthenticated

#importing the models we created to the views so we could refer to them here to perform certain actions

from .models import Category, MenuItem, Cart, Order, OrderItem

#Importing serializers we created at serializers.py
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerilializer

# The line below imports the RESPONSE method for the RETURN method.
# It is used as a way to send a response from the server to the client in the form of a serialized data structure, such as JSON or XML.
# It also allows the server to include additional information such as HTTP status codes and headers in the response.
# Response also helps with formatting the response so it can be easily consumed by the client.
from rest_framework.response import Response

# The line below imports the IsAdminUser permission which checks if the user accessing the func is an Admin
from rest_framework.permissions import IsAdminUser, BasePermission

# The line below import the method used to return an object or if the objects doesn't exist return thr 404 error
from django.shortcuts import  get_object_or_404

# The line below imports the built in Group and USER models, that are created automatically by django
from django.contrib.auth.models import Group, User

# Imports the VIEWSETS that are used similar way as APIView class but requires less code to write
from rest_framework import viewsets

# Imports the status method which is able to return an HTTP result status e.g. status.HTTP_403_Forbidden or status.HTTP_404_NOTFOUND
from rest_framework import status, permissions


#The class below is a custom permission method that I've created that checks of the user belongs to superuser or to a manager group..
#..if so the return of the function will be TRUE which will allow actions
#The class is used at get_permissions func at any view
class IsManagerOrSuper(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()



class CategoriesView(generics.ListCreateAPIView):
    #ListCreateAPIView requires 2 args - queryset which represnts model and serializer class
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrSuper]

        return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrSuper]

        return [permission() for permission in permission_classes]





class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    #The line below allows us a search for items by title of the category
    search_fields = ['category__title']
    #The line below allows us ordering by either price or inventory (if we remove that, that ordering will be performed across all fields of Model)
    ordering_fields = ['price', 'inventory']


    #Below is a function that used to get the permissions that are required for a certain request.
    def get_permissions(self):
        #below declares an empty list to store the permission classes.
        permission_classes = []
        #below line is to check if the request method is not equal to 'GET'
        if self.request.method != 'GET':
            #the line below acts If the request method is not 'GET', then it adds the IsManagerOrSuper permission class to the list.
            permission_classes = [IsManagerOrSuper]
        #below line returns a list of permission classes that are needed based on the request method.
        #It does this by looping through the permission_classes list and creating an instance of each permission class.
        #Without it, the function won't work
        return [permission() for permission in permission_classes]








class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrSuper]

        return [permission() for permission in permission_classes]








class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    #By default LisrCreateAPIView will display all the items situated at the Cart model, we use the func below to specify conditions for GET method.. 
    #..which items to display In this case we get all the items and filter them by the specific User currently accessing the Cart API
    #We still use the 'queryset' variable at the beggining cuz it's mandatory for the ListCreateAPIView method
    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    #This func enables to perform the DELETE request which will delete all the items filtered to a specific user currently using the Cart API
    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")











class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    #The func below is used to specify queryset we get with conditions depending on the code inside the func
    def get_queryset(self):

        #Below we set specific conditions to the queryset, check if the user is admin (superuser) and then perform the action of displaying..
        #..all items in the Orders
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: #normal customer doesn't below to the group therefore has count of 0 accroding to the biult in..
            #..Groups model, then we return the items specific to that user
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): #Filterin the users belonging only to the group "Delivery Crew"
            return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to a specific delivery crew member
        else: #delivery crew or manager
            return Order.objects.all() #If a user accesig belongs to another group other than 0, delivery crew

    #Func that specifies the conditions for the create method. It is used to create and order from the items stored in a user's cart.
    # 1)  if the objects in the Cart belonging to a specific user =0 then we display a message "no items in cart"
    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})


        #2) A copy of the data passed to POST request is assigned to the variable data for possible manipulation of data to modify fields below.

        # For example, if a developer wants to add some additional parameters to the request data dictionary..
        # ..they can make a shallow copy of the dictionary and add the additional parameters to the copy, instead of adding the parameter..
        # ..directly to the original dictionary. This ensures that the original request data dictionary remains unchanged.
        data = request.data.copy()
        #3) The total price of the items in the user's cart is calculated using get_total_price func below and stored in the total variable.
        total = self.get_total_price(self.request.user)
        #4) The calculated total is added to the data as a key-value pair. This becomes our value at OrderSerializer for the field "total"
        data['total'] = total
        #5) The user ID associated with the request is added to the data as a key-value pair.This becomes our value at OrderSerializer for the field "user"
        data['user'] = self.request.user.id
        #6) The data is then passed to the OrderSerializer to be validated.
        order_serializer = OrderSerializer(data=data)#in brackets here first "data" is mandatory and always has that name, second is our variable..
        #..which we defined above and could use another name

        #7) If the data is valid, the fields get a value assigned from the data we have designed above and then it gets saved.
        if (order_serializer.is_valid()):
            order = order_serializer.save()
            #8) The items in the user's cart are retrieved belonging to a user who made a request
            items = Cart.objects.all().filter(user=self.request.user).all()
            #9) For each item in the cart, an OrderItem is created and saved referrign to the menuitem_id, price and quantity
            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()
            # 10) after the number 9 all the items belongign to a user in his Cart get deleted
            Cart.objects.all().filter(user=self.request.user).delete()
            # 11) A copy of the order serializer data is stored in the result variable to manipulate the total data below
            result = order_serializer.data.copy()
            # 12) The calculated total is added to the result as a key-value pair.
            result['total'] = total
            # 13) Returns the data we get as the result at order_serializer
            return Response(order_serializer.data)



    # The func that calculates the total field
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total













class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    #specifying the conditions for the update (put / patch method)
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
            return Response('Not Ok')
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)














#thIS class is to modify users belonging to managers' group
class GroupViewSet(viewsets.ViewSet):
    # Using the viewsets we need to specify the action for used HTTP requests. For that we use def LIST (GET), def create (POST),def destroy (DELETE)
    #.. The names of the functions are always the same for any viewset
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)
















class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery Crew')
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)