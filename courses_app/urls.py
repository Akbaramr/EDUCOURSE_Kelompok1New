from django.urls import path
from courses_app import views


app_name = 'courses_app'


urlpatterns = [
    path('', views.index, name='index'),
    path('search',views.search,name='search')
]