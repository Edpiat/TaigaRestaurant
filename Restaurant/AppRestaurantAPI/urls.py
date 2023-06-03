from django.urls import path
from . import views

urlpatterns = [
    #This is how we map class based views to the URLS, the difference with the function based views is that here we add ".as_view()" at the end
    path('categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    #Below is the same as above, but here <int:pk> specifies that at the end of url user adds a number of the specific number and goes there
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),



    #Below are the paths that connect class based viewsets to URLS, in the brackers we map the functions of that classes that we have defined in
    #the views.py file. So we specify that e.g. "def list" func at "GroupViewSet" inside the "VIEWS.py file acts for the GET HTTP method and so on.
    path('groups/manager/users', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),

    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}))
]