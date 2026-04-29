from django.urls import path, re_path, register_converter
from . import views
from arcada.converters import FourDigitYearConverter 

register_converter(FourDigitYearConverter, 'year4')  

urlpatterns = [
    path('', views.index, name='home'),
    path('game/<int:game_id>/', views.categories, name='game_id'),
    path('game/<slug:game_slug>/', views.categories_by_slug, name='game'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    path('archive/<year4:year>/', views.archive, name='archive_conv'),
    path('old-archive/', views.old_archive, name='old_archive'),
    path('reverse-example/', views.reverse_example, name='reverse_example'),
]