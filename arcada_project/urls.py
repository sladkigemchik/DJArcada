from django.contrib import admin
from django.urls import path, include
from arcada.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('arcada.urls')),
]
