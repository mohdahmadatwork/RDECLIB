from django.urls import include, path

from publicview import views
urlpatterns = [
    path('',views.publichome,name='Home')
]