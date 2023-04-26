from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=250)
    qty = models.IntegerField()
    price = models.FloatField()
    author = models.CharField(max_length=250)
    is_published= models.BooleanField(default=True) 
    is_active= models.BooleanField(default=True) 


    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = "book"


class Upload_Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    pdfs = models.FileField(upload_to= 'uploadedBooks/pdfs/')
    cover = models.ImageField(upload_to= 'uploadedBooks/covers/',null=True,blank=True)

    def __str__(self):
        return self.title
    
    def delete(self,*args,**kwargs):
        self.pdfs.delete()
        self.cover.delete()
        return super().delete(*args,**kwargs)