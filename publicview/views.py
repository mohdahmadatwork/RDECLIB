from django.shortcuts import render,HttpResponse

# Create your views here.
def publichome(request):
    return render(request, "publicviewindex.html")