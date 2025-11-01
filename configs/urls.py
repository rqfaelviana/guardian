"""
URL configuration for configs project.

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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. URLs de Autenticação (Login, Logout, etc.)
    #    Isso cria: /api/auth/login/, /api/auth/logout/, etc.
    path('api/auth/', include('dj_rest_auth.urls')), 
    
    # 3. URLs de Registro
    #    Isso cria: /api/auth/registration/
    #    Este endpoint usará automaticamente o seu 'CustomRegisterSerializer'
    #    porque o configuramos no settings.py
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
