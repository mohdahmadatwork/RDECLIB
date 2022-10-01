from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from dashboard.resources import PropertyAdminResource
# Register your models here.
from dashboard.models import AddBook,AddStudent, Book_Return,Book_issued,faculty
class AddbookAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = PropertyAdminResource
    
    
admin.site.register(AddBook,AddbookAdmin)
admin.site.register(AddStudent)
admin.site.register(Book_issued)
admin.site.register(Book_Return)
admin.site.register(faculty)