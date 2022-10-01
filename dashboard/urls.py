from hashlib import new
from django.urls import path

from dashboard import views

urlpatterns = [
    path('',views.dashboard,name="Dashboard"),
    path('addbook/',views.addbook,name="Add Books"),
    path('opac/all/',views.showbook,name="OPAC"),
    path("bookadding/",views.addbooksub,name="BookAddedFormSubmit"),
    path('reports/',views.reports,name="Reports"),
    path("addstudent/",views.studentadd,name="Student Add"),
    path("showstudent/",views.showstudent,name="showstudent"),
    path("bookissue/<str:Lib_id>",views.bookissued,name="bookissued"),
    path("studentprofile/<str:Lib_id>",views.studentprofile,name="studentprofile"),
    path("bookreturn/<str:Lib_id>",views.bookreturn,name="studentprofile"),
    path("removeprofile/<str:Lib_id>",views.removeprofile,name="removeprofile"),
    path("error/",views.error,name="error"),
    path("booksearch/",views.booksearch,name="booksearch"),
    path("studentsearch/",views.studentsearch,name="studentsearch"),
    path("showrequestedfaculty/",views.showrequestedfaculty,name="showrequestedfaculty"),
    path("confirmfaculty/<str:Username>",views.confirmfaculty,name="confirmfaculty"),
    path("unconfirmfaculty/<str:Username>",views.unconfirmfaculty,name="unconfirmfaculty")
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
