"""
URL configuration for CER2DIAZJOSE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('materiales/', views.materiales, name='materiales'),
    path('puntos-limpios/', views.puntos_limpios, name='puntos_limpios'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('metricas/', views.metricas, name='metricas'),
    path('registro/', views.registro, name='registro'),
    path('solicitud/nueva/', views.nueva_solicitud, name='nueva_solicitud'),

]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
