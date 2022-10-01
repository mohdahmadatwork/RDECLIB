from django.shortcuts import render,HttpResponse
from dashboard.models import AddStudent,AddBook,Book_issued,Book_Return
# Create your views here.
def studentdashboard(request,str):
    student = AddStudent.objects.filter(Library_ID = str).first()
    bookstaken = Book_issued.objects.filter(Student = student)
    booksreturn = Book_Return.objects.filter(Student = student)
    studentdata = {"student":student,"bookstaken":bookstaken,"booksreturn":booksreturn}
    return render(request,"studentdashboard.html",studentdata)

def studentprofile(request,str):
    student = AddStudent.objects.filter(Library_ID = str).first()
    bookstaken = Book_issued.objects.filter(Student = student)
    booksreturn = Book_Return.objects.filter(Student = student)
    studentdata = {"student":student,"bookstaken":bookstaken,"booksreturn":booksreturn}
    return render(request,"student-profile2.html",studentdata)