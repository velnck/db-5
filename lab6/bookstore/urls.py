from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='catalog/books'), name='main'),
    path('catalog/', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
]
