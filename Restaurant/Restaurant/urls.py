"""
URL configuration for Restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

#Importing path for views and include to include apps' urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #include to include apps' urls.py
    path('api/', include ('AppRestaurantAPI.urls')),

    #path that enables djoser built in urls for authentication
    path('auth/', include('djoser.urls')),

    #path that enables authentication with djosers authtoken
    path('auth/', include('djoser.urls.authtoken')),
]






#9) Reffering to the DJOSER lib


# Djoser offers a few handy endpoints. Here is a list of them.:
#   These endpoints are accessible at specified location in the PROJECT URLS you added, in this example: auth/
#   So to access the endpoint need e.g.: /auth/users/

#9.1)/users/

   # lists all the users and you can make a post call to create a new one.
   # If you want to create a new user from an API client like insomnia, you don't need to pass any token to this API.


#9.2) /users/me

   # auth users me end point, make it get call with any user's token to this end point, and it will provide the details of the authenticated user.
   # This endpoint also supports a put call to update the email address of this user.

#9.3) /users/confirm/
#9.4) /users/resend_activation/
#9.5) /users/set_password/
#9.6) /users/reset_password/
#9.7) /users/reset_password_confirm/
#9.8) /users/set_username/
#9.9) /users/reset_username/
#9.10) /users/reset_username_confirm/
#9.11) /token/login/

   #You can also create tokens for a user from the auth/token/login endpoint.
   #You can use insomnia to make an HTTP post call with username and password and receive the token, or you can use the browsable API view.
   #There is a form with username and password fields that you can use to generate user tokens

#9.12) /token/logout/





#Some of them support only GET calls, some All avalable calls



#If you visit the /aut/users/ endpoint and want to add new users, then you need to login as a superuser in the Django admin first.
# Then you can visit these browsable API endpoints.



