from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                          # Админка
    path('', include('core.urls')),                           # Твои основные страницы
    path('accounts/', include('django.contrib.auth.urls')),  # Аутентификация: login/logout
]
