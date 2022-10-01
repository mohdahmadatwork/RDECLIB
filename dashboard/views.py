# from urllib import request
from email import message
from django.shortcuts import redirect, render
# from django.template import Library
from dashboard.models import AddBook, Book_Return,Book_issued,AddStudent,faculty
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import qrcode
from uuid import uuid4
import os
from rdeclib2 import settings
# from . import User
# Create your views here.
def error(request):
    return render(request,"error.html")
def countbook(author,title):
    count = 0
    for i in AddBook.objects.all().filter(Title=title,Author=author):
        if i.Available:
            count+=1
    return count

def GenLibId(RollNumber,objid):
    pass



# Func for finding books in demanding
def BookDemand():
    booksdemand=Book_issued.objects.all()
    allbooks=AddBook.objects.all()
    issuedbook=[]
    count=0
    for book1 in allbooks:
        countbook=[]
        for book2 in allbooks:
            if book1.Author == book2.Author and book1.Title == book2.Title:
                if book1.Available == False:
                    count+=1
        countbook.append(count)
        countbook.append(book1)
        issuedbook.append(countbook)
        count = 0 
    lstofpop=[]
    for i in range(len(issuedbook)):
        for j in range(len(issuedbook)):
            if i!=j:
                if j not in lstofpop:
                    if issuedbook[i][1].Author==issuedbook[j][1].Author and issuedbook[i][1].Title==issuedbook[j][1].Title:
                        lstofpop.append(i)
    newlst=[]
    for i in range(len(issuedbook)):
        if i not in lstofpop:
            newlst.append(issuedbook[i])
    return newlst
def dashboard(request):
    if request.user.is_authenticated:
        usercount=len(User.objects.all())
        
        books=AddBook.objects.all().order_by('-Date')
        newbookscount=len(books)
        books=books[0:10]
        recentbook=[]
        for book in books:
            lstofcount=[]
            count=countbook(book.Author,book.Title)
            lstofcount.append(count)
            lstofcount.append(book)
            if count==0:
                lstofcount.append("Not Available")
                lstofcount.append("danger")
            else:
                lstofcount.append("Available")
                lstofcount.append("success")

            recentbook.append(lstofcount)
        # print(recentbook)   
        lstofpop=[]
        for i in range(len(recentbook)):
            for j in range(len(recentbook)):
                if i!=j:
                    if j not in lstofpop:
                        if recentbook[i][1].Author==recentbook[j][1].Author and recentbook[i][1].Title==recentbook[j][1].Title:
                            lstofpop.append(i)
        newlst=[]
        for i in range(len(recentbook)):
            if i not in lstofpop:
                newlst.append(recentbook[i])
        # print(newlst)
        demandingbooks=BookDemand()

        #set of faculty object for the confirmation for the faculty
        ffc = GiveAllObjOfRequestedFaculty(request.user) #ffc- faculty for the confirmation
        #variable for finding the count of the ffc
        countffc = len(ffc)
        mydict={"books":newlst,
                "usercount":usercount,
                "newbookscount":newbookscount,
                "bookissued":len(Book_issued.objects.all()) ,
                "bookindemands":demandingbooks,
                'ffc':ffc,
                "countffc":countffc ,
                
                }
        return render(request,"dashboard.html",mydict)
    else:
        return redirect("/")
#Function for the showing the faculty data requested for confirmation
def GiveAllObjOfRequestedFaculty(user):
    userfaculty = faculty.objects.filter(Username=user.username).get() #ffc- faculty for the confirmation
    if userfaculty.Designation in ('Dean','Director'):
        #set of faculty object for the confirmation for the faculty
        ffc = faculty.objects.filter(Confirm = False) #ffc- faculty for the confirmation
    elif userfaculty.Designation in ('HOD'):
        ffc = faculty.objects.filter(Confirm = False).filter(Branch = user.faculty.Branch) #ffc- faculty for the confirmation
    else:
        ffc = ""
    return ffc
def showrequestedfaculty(request):
    ffc = GiveAllObjOfRequestedFaculty(request.user)
    return render(request,"showrequestedfaculty.html",{'ffc':ffc})

#Function for confirming the faculty
def confirmfaculty(request,Username):
    ffc = faculty.objects.filter(Username=Username).get()
    ffc.Confirm=True
    ffc.save()
    messages.success(request,Username+" can access Library Now.")
    return redirect("/clgsite/")

#Function for not confirmed faculty
def unconfirmfaculty(request,Username):
    ffc = faculty.objects.filter(Username=Username).get()
    ffcuser = ffc.customuser
    ffcuser.delete()
    ffc.delete()
    messages.success(request, Username+" can no longer be able to access library")
    return redirect("/clgsite/")    


def addbook(request):
    return render(request,"forms-layouts.html")

def showbook(request):
    books=AddBook.objects.all().order_by('-Date')
    recentbook=[]
    for book in books:
        lstofcount=[]
        count=countbook(book.Author,book.Title)
        lstofcount.append(count)
        lstofcount.append(book)
        if(count==0):
            status="Not Available"
            lstofcount.append(status)    
            lstofcount.append("danger")

        elif(count >0 and count<4):
            status="Few"
            lstofcount.append(status)    
            lstofcount.append("warning")
        else:
            status="Available"
            lstofcount.append(status)    
            lstofcount.append("success")
        recentbook.append(lstofcount)
        
    # print(recentbook)   
    lstofpop=[]
    for i in range(len(recentbook)):
        for j in range(len(recentbook)):
            if i!=j:
                if j not in lstofpop:
                    if recentbook[i][1].Author==recentbook[j][1].Author and recentbook[i][1].Title==recentbook[j][1].Title:
                        lstofpop.append(i)
    newlst=[]
    for i in range(len(recentbook)):
        if i not in lstofpop:
            newlst.append(recentbook[i])
    # print(newlst)
    return render(request,"tables-data.html",{"books":newlst})
def addbooksub(request):
    if request.method == "POST":
        booknumber=request.POST["booknumber"]
        if len(AddBook.objects.all().filter(Book_Number=booknumber))!=0:
            messages.success(request,"Book number is already present")
            return redirect("/clgsite/addbook/")
        try:
            boolean=request.POST["aslikeprev"]
        except MultiValueDictKeyError:
            boolean="off"
        print(boolean)
        if boolean=="on":
            books=AddBook.objects.all().latest('Date')
            if len(request.POST["remark"])==0:
                remark=books.Remark
            else:
                remark=request.POST["remark"]
            if len(request.POST["withdrawndate"])==0:
                withdrawndate=books.Withdrawn_Date
            else:
                withdrawndate=request.POST["withdrawndate"]
            if len(request.POST["billdate"])==0:
                billdate=books.Bill_Date
            else:
                billdate=request.POST["billdate"]
            if len(request.POST["billnumber"])==0:
                billnumber=books.Bill_Number
            else:
                billnumber=request.POST["billnumber"]
            if len(request.POST["classnumber"])==0:
                classnumber=books.class_No
            else:
                classnumber=request.POST["classnumber"]
            
            if len(request.POST["pages"])==0:
                pages=books.Pages
            else:
                request.POST["pages"]
            if len(request.POST["publisher"])==0:
                publisher=books.Publisher
            else:
                publisher=request.POST["publisher"]
            if len(request.POST["place"])==0:
                place=books.Place
            else:
                place=request.POST["place"]
            if len(request.POST["source"])==0:
                source=books.Source
            else:
                source=request.POST["source"]
            if len(request.POST["yearofpublication"])==0:
                yearofpublication=books.Year_Of_Publication
            else:
                yearofpublication=request.POST["yearofpublication"]
            if len(request.POST["volume"])==0:
                volume=books.Volume
            else:
                volume=request.POST["volume"]
            if len(request.POST["title"])==0:
                title=books.Title
            else:
                title=request.POST["title"]
            if len(request.POST["author"])==0:
                author=books.Author
            else:
                author=request.POST["author"]
            if len(request.POST["date"])==0:
                date=books.Date
            else:
                date=request.POST["date"]
            if len(request.POST["category"])==0:
                category=books.Category
            else:
                category=request.POST["category"]
            print(category)
            book=AddBook(Date = date,Author = author,Title = title,Volume = volume,Place = place,Publisher = publisher,Year_Of_Publication = yearofpublication,Source = source,Pages = pages,Book_Number = booknumber,Bill_Number = billnumber,Bill_Date = billdate,Withdrawn_Date = withdrawndate,Remark = remark,class_No=classnumber,Category=category)
            book.save()
            messages.success(request,"Book is successfully Added")
            return redirect("/clgsite/addbook/")
        else:
            remark=request.POST["remark"]
            withdrawndate=request.POST["withdrawndate"]
            billdate=request.POST["billdate"]
            billnumber=request.POST["billnumber"]
            classnumber=request.POST["classnumber"]
            booknumber=request.POST["booknumber"]
            pages=request.POST["pages"]
            publisher=request.POST["publisher"]
            place=request.POST["place"]
            source=request.POST["source"]
            yearofpublication=request.POST["yearofpublication"]
            volume=request.POST["volume"]
            title=request.POST["title"]
            author=request.POST["author"]
            date=request.POST["date"]
            print(date,author,title,volume,yearofpublication,source,publisher,pages,booknumber,classnumber,billnumber,billdate,withdrawndate,remark)
            book=AddBook(Date = date,Author = author,Title = title,Volume = volume,Place = place,Publisher = publisher,Year_Of_Publication = yearofpublication,Source = source,Pages = pages,Book_Number = booknumber,Bill_Number = billnumber,Bill_Date = billdate,Withdrawn_Date = withdrawndate,Remark = remark,class_No=classnumber)
            book.save()
    return redirect("/clgsite/addbook/")

def reports(request):
    books=AddBook.objects.all().order_by('Date')
    books=books[0:10]
    recentbook=[]
    for book in books:
        lstofcount=[]
        lstofcount.append(countbook(book.Author,book.Title))
        lstofcount.append(book)    
        recentbook.append(lstofcount)
    # print(recentbook)   
    lstofpop=[]
    for i in range(len(recentbook)):
        for j in range(len(recentbook)):
            if i!=j:
                if j not in lstofpop:
                    if recentbook[i][1].Author==recentbook[j][1].Author and recentbook[i][1].Title==recentbook[j][1].Title:
                        lstofpop.append(i)
    newlst=[]
    for i in range(len(recentbook)):
        if i not in lstofpop:
            newlst.append(recentbook[i])
    # print(newlst)
    return render(request,"report.html",{"books":newlst})

def studentadd(request):
    if request.method=="POST":
        t=AddStudent()
        t.First_Name=request.POST["firstname"]
        t.Last_Name=request.POST["lastname"]
        t.Fathers_Name=request.POST["fathersname"]
        t.Address=request.POST["address"]
        t.Roll_Number=request.POST["rollnumber"]
        t.Year=request.POST["year"]
        t.Branch=request.POST["branch"]
        t.Phone_Number=request.POST["phonenumber"]
        t.Joining_Date=request.POST["joiningdate"]
        t.Expiring_Date=request.POST["expiringdate"]
        # form = studentForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        #     return redirect("/clgsite/")
        if(len(request.FILES["studentimage"])!=0):
            t.Student_image=request.FILES["studentimage"]
        
        t.Library_ID="RDEC"+t.Branch[0:1]+str(t.Year)+str(t.objectid)
        password = "rdec@123"
        myuser = User.objects.create_user(t.Library_ID,password)
        myuser.save()
        t.customuser = myuser
        t.save()
        # student=AddStudent(First_Name = First_Name,Last_Name =Last_Name,Fathers_Name =Fathers_Name,Address =Address,Roll_Number =Roll_Number,Year =Year,Branch =Branch,Phone_Number =Phone_Number,Joining_Date =Joining_Date,Expiring_Date =Expiring_Date,Student_image=Student_image)
        # student.save()
        print(t)
        return redirect("/clgsite/")
    return render(request,"studentadd.html")

def barcode(studentlibid):
    features = qrcode.QRCode(version=1,box_size=100,border=2)
    url="http://127.0.0.1:8000/clgsite/studentprofile/"+str(studentlibid)
    features.add_data(url)
    features.make(fit=True)
    generate_image=features.make_image(fill_color='black',back_color='white')
    # generate_image.save(str(studentlibid))
    generate_image.save(settings.MEDIA_ROOT + '/' + str(studentlibid))
    return generate_image

def path_and_rename(instance, filename):
    upload_to = 'img'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def showstudent(request):
    student=AddStudent.objects.all()
    return render(request,"showstudent.html",{"students":student})

def bookissued(request,Lib_id):
    if request.method=="POST":
        bn=request.POST["bn"]
        student=AddStudent.objects.filter(Library_ID= (Lib_id)).first()
        book=AddBook.objects.filter(Book_Number=bn).first()
        if book.Available:
            bi=Book_issued()
            bi.bookno=book
            bi.Student=student
            bi.save()
            book.Available=False
            book.save()
            messages.success(request,"Book Issued Successfully")
            return redirect("/clgsite/studentprofile/"+Lib_id)
        else:
            messages.success(request,"Book Is not available")
            return redirect("/clgsite/studentprofile/"+Lib_id)
    else:
        return redirect("/clgsite/error/")

def bookreturn(request,Lib_id):
    if request.method=="POST":
        bn=request.POST["bn"]
        book=AddBook.objects.filter(Book_Number=bn).first()
        if book.Available==False:
            bissued=Book_issued.objects.filter(bookno=book).order_by("-Date_Issue").first()
            if bissued.Student.Library_ID== ((Lib_id)):
                if  bissued.Date_Return==None:
            # student=Book_issued
                    br=Book_Return()
                    br.bookno=book
                    br.Student=bissued.Student
                    br.save()
                    bissued.Date_Return=br.Date_Return
                    bissued.save()
                    book.Available=True
                    book.save()
                    messages.success(request,"Book successfully Returned")
                else:
                    messages.success(request,"Book is already Returned")
            else:
                messages.success(request,"Book is not issued to this student")
        else:
            messages.success(request,"Book Not Returned")

        # return redirect("/clgsite/studentprofile/{Lib_id}")
        
    return redirect("/clgsite/studentprofile/"+Lib_id)

def studentprofile(request,Lib_id):
    student=AddStudent.objects.filter(Library_ID= (Lib_id)).first()
    # student=student.get()
    print(student)
    book_issued=Book_issued.objects.filter(Student=student)
    print(book_issued)
    lst=[]
    for i in book_issued:
        lst.append(i.bookno)
    print(lst)
    return render(request,"Student-profile.html",{"History":book_issued,"student":student})

def editstudentprofile(request,Lib_id):
    if request=="POST":
        student=AddStudent.objects.filter(Library_ID=int(Lib_id)).get()
        # student.F
        pass
    pass

def removeprofile(request,Lib_id):
    student=AddStudent.objects.filter(Library_ID=int(Lib_id)).first()
    student.Student_Image= "None"
    student.save()
    return redirect("/clgsite/studentprofile/"+(Lib_id))

# Book Search function
def booksearch(request):
    if request.method == "POST":
        keyword=request.POST.get("query")
        # print(keyword)
        filterkey=request.POST["queryfilter"]
        # print(filterkey)
        if filterkey=="Author":
            books=AddBook.objects.all().filter(Author__contains=keyword)
        elif filterkey=="Title":
            books=AddBook.objects.all().filter(Title__contains=keyword)
        elif filterkey=="Accession_Number":
            books=AddBook.objects.all().filter(Accession_Number__contains=int(keyword))
            
        elif filterkey=="Date":
            books=AddBook.objects.all().filter(Date__contains=keyword)
        
        elif filterkey=="Volume":
            books=AddBook.objects.all().filter(Volume__contains=keyword)
            
        elif filterkey=="Place":
            books=AddBook.objects.all().filter(Place__contains=keyword)
            
        elif filterkey=="Publisher":
            books=AddBook.objects.all().filter(Publisher__contains=keyword)
            
        elif filterkey=="Year_Of_Publication":
            books=AddBook.objects.all().filter(Year_Of_Publication__contains=keyword)
        
        elif filterkey=="Source":
            books=AddBook.objects.all().filter(Source__contains=keyword)
            
        elif filterkey=="Pages":
            books=AddBook.objects.all().filter(Pages=int(keyword))
            
        elif filterkey=="Book_Number":
            books=AddBook.objects.all().filter(Book_Number=int(keyword))
            
        elif filterkey=="Bill_Number":
            books=AddBook.objects.all().filter(Bill_Number=int(keyword))
        elif filterkey=="Bill_Date":
            books=AddBook.objects.all().filter(Bill_Date=keyword)
        
        elif filterkey=="Withdrawn_Date":
            books=AddBook.objects.all().filter(Withdrawn_Date=keyword)
        
        elif filterkey=="Category":
            books=AddBook.objects.all().filter(Category=keyword)
        elif filterkey=="Available":
            books=AddBook.objects.all().filter(Available=True)
        recentbook=[]
        for book in books:
            lstofcount=[]
            count=countbook(book.Author,book.Title)
            lstofcount.append(count)
            lstofcount.append(book)
            if(count==0):
                status="Not Available"
                lstofcount.append(status)    
                lstofcount.append("danger")

            elif(count >0 and count<4):
                status="Few"
                lstofcount.append(status)    
                lstofcount.append("warning")
            else:
                status="Available"
                lstofcount.append(status)    
                lstofcount.append("success")
            recentbook.append(lstofcount)
            
        # print(recentbook)   
        lstofpop=[]
        for i in range(len(recentbook)):
            for j in range(len(recentbook)):
                if i!=j:
                    if j not in lstofpop:
                        if recentbook[i][1].Author==recentbook[j][1].Author and recentbook[i][1].Title==recentbook[j][1].Title:
                            lstofpop.append(i)
        newlst=[]
        for i in range(len(recentbook)):
            if i not in lstofpop:
                newlst.append(recentbook[i])
        # print(newlst)
        messages.success(request,"Search Results: ")
        return render(request,"tables-data.html",{"books":newlst})    

# Student Search Function
def studentsearch(request):
    if request.method=="POST":
        keyword=request.POST.get("query")
        filterkey=request.POST.get("queryfilter")
        print(keyword)
        print(filterkey)
        if filterkey=="First_Name":
            student=AddStudent.objects.all().filter(First_Name__contains=keyword)

        elif filterkey=="Last_Name":
            student=AddStudent.objects.all().filter(Last_Name__contains=keyword)
            
        elif filterkey=="Fathers_Name":
            student=AddStudent.objects.all().filter(Fathers_Name__contains=keyword)
            
        elif filterkey=="Address":
            student=AddStudent.objects.all().filter(Address__contains=keyword)
            
        elif filterkey=="Roll_Number":
            student=AddStudent.objects.all().filter(Roll_Number__contains=keyword)
            
        elif filterkey=="Year":
            student=AddStudent.objects.all().filter(Year__contains=keyword)
            
        elif filterkey=="Branch":
            student=AddStudent.objects.all().filter(Branch__contains=keyword)
            
        elif filterkey=="Phone_Number":
            student=AddStudent.objects.all().filter(Phone_Number__contains=keyword)
            
        elif filterkey=="Joining_Date":
            student=AddStudent.objects.all().filter(Joining_Date__contains=keyword)
            
        elif filterkey=="Expiring_Date":
            student=AddStudent.objects.all().filter(Expiring_Date__contains=keyword)
            
        elif filterkey=="Library_ID":
            student=AddStudent.objects.all().filter(Library_ID__contains=keyword)
            
        elif filterkey=="Student_image":
            student=AddStudent.objects.all().filter(Student_image__contains=keyword)
            
        elif filterkey=="Email":
            student=AddStudent.objects.all().filter(Email__contains=keyword)

        return render(request,"showstudent.html",{"students":student})


def NormalFacultyDashboard(request):
    pass