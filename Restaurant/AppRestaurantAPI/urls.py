from django.urls import path
from . import views

urlpatterns = [
    #This is how we map class based views to the URLS, the difference with the function based views is that here we add ".as_view()" at the end
    
    #The below path leads us to the categories our restaurant has
    path('categories', views.CategoriesView.as_view()),
    #The path below let's us see and modify the exact category referring to its ID
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    #The path below leads us to the menuitems our restaurant has
    path('menu-items', views.MenuItemsView.as_view()),
    #Below is the same as above, but here <int:pk> specifies that at the end of url user adds a number of the specific number and goes there
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    #The path below leads us to the CART of a specific user
    path('cart/menu-items', views.CartView.as_view()),
    #The path below leads us to the page with orders to see or create
    path('orders', views.OrderView.as_view()),
    #The path below let's us see and modify the exact order referring to its ID
    path('orders/<int:pk>', views.SingleOrderView.as_view()),



    #Below are the paths that connect class based viewsets to URLS, in the brackers we map the functions of that classes that we have defined in
    #the views.py file. So we specify that e.g. "def list" func at "GroupViewSet" inside the "VIEWS.py file acts for the GET HTTP method and so on.
    path('groups/manager/users', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),

    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}))
]