"""
URL configuration for exp project.

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
from django.urls import path
from user.views import blockchain,init,results,posselection
from main.views import homepage,creatorpage,startpage,votersreg,minersreg,demopage
from mine.views import mining,demomine
from . views import vews,register,loginUser,LogoutUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vews,name='home'),
    path('register/',register,name='register'),
    path('login/',loginUser,name='login'),
    path('logout/',LogoutUser,name='logout'),
    path('create/',demopage,name='create'),
    path('voters/',init,name='init'),
    path('voters/select/',posselection,name='select'),
    path('voters/select/vote/',blockchain,name='vote'),
    path('voters/select/vote/results/',results,name='results'),
    path('mining/',demomine,name='mining'),
    ]
