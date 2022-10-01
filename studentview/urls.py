from django.urls import include, path
from studentview import views
urlpatterns = [
    path('',views.studentdashboard,name="Student Home"),
    path('myprofile/',views.studentprofile,name="My profile")
]