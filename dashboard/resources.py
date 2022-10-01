from import_export import resources
from dashboard.models import AddBook

class PropertyAdminResource(resources.ModelResource):

    class Meta:
        model   =   AddBook
        raise_errors = False
        import_id_fields = ("Date", "Accession_Number", "Author", "Title", "Volume", "Place", "Publisher", "Year_Of_Publication", "Source", "Pages", "Book_Number", "Bill_Number", "Bill_Date","Withdrawn_Date", "Remark", "class_No")