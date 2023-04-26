from django.shortcuts import render,HttpResponse,redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Book

from django.contrib.auth.decorators import login_required





@csrf_exempt
@login_required # type: ignore
def home(request):
    if request.method == "POST":
        bid = request.POST.get('book_id')
        name = request.POST.get("book_name")
        qty = request.POST.get("book_qty")
        price = request.POST.get("book_price")
        author = request.POST.get("book_author")
        is_pub = request.POST.get("book_is_pub")
        # print(name,qty,price,author,is_pub)
        if is_pub == "Yes":
             is_pub = True
        else:
             is_pub=False

        if not bid:     
          Book.objects.create(name=name , qty=qty , price=price , author=author, is_published=is_pub)
        else:
             book_obj=Book.objects.get(id=bid)
             book_obj.name = name
             book_obj.qty = qty
             book_obj.price = price
             book_obj.author = author
             book_obj.is_published = is_pub
          
             book_obj.save()

        return redirect('home')
        # print("one  = ",request.method )
        # return HttpResponse('success')
    elif request.method == "GET":
        # print("two  = ",request.method )
        return render(request ,"home.html")
    

@login_required # type: ignore
def show_books(request):
     return render(request , "show_books.html",{"all_books":Book.objects.filter(is_active=True)})

@login_required # type: ignore
def show_inactive_books(request):
     return render(request , "show_books.html", {"all_books":Book.objects.filter(is_active=False),"inactive": True}) 

@login_required # type: ignore
def recover_book(request,pk):
     book_obj = Book.objects.get(id=pk)
     book_obj.is_active = True
     book_obj.save()
     return redirect('active_books')




@login_required # type: ignore
def update_book(request,pk):
     book_obj = Book.objects.get(id=pk)
     return render(request ,"home.html",context={'single_book': book_obj})



@login_required # type: ignore
def hard_delete(request,pk):
     Book.objects.get(id=pk).delete()
     return redirect('active_books')

@login_required # type: ignore
def soft_delete(request,pk):
     book_obj = Book.objects.get(id=pk)
     book_obj.is_active = False
     book_obj.save()
     return redirect('active_books')



import csv

@login_required # type: ignore
def create_csv(request):
     response = HttpResponse(content_type='text/csv')
     response['Content-Disposition'] = 'attachment; filename=test.csv'

     writer = csv.writer(response)
     writer.writerow(['name','qty','price','author','is_published','is_active'])

     books = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
     for book in books:
          writer.writerow(book)
     return response

# import pandas as pd
# # def upload_csv(request):
#      # file = request.FILES['csv_file']
#      # decoded_file = file.read().decode('utf-8').splitlines()
     
#      # reader =csv.DictReader("decoded_file")
#      # for element in reader:
#           # print(element)
#      # return HttpResponse('succ') #not working


@login_required # type: ignore
def upload_csv(request):
    file = request.FILES["csv_file"]
    data = file.read().decode('unicode_escape').splitlines()
    
    reader = csv.DictReader(data)
    lst1 = []
    for element in reader:             #True string mein aayegaa isliye isko karna padaga
        is_pub = element.get("is_published")
        if is_pub == "TRUE":
            is_pub = True
            
        is_act = element.get("is_active")    #same as is_published , is_active ke liye bhi
        if is_act == "TRUE":
            is_act = True 
            lst1.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"),author=element.get("author"), is_published=is_pub,is_active=is_act))

        
    Book.objects.bulk_create(lst1)   
    return HttpResponse("Successful")


#################################################################################


@login_required # type: ignore
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'qty','price','author','is_published','is_active'])
    return response


###############################################################################





# simple upload     
@login_required # type: ignore
def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name , uploaded_file)
        context['url'] = fs.url(name)

        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, "upload.html",context=context)





##########################--FUNCTION BASED UPLOAD ---########################################################

from .forms import BookForm
from .models import Upload_Book

@login_required # type: ignore
def book_list(request):
        books = Upload_Book.objects.all()
        return render(request, "book_list.html",{"books":books})


@login_required # type: ignore
def upload_books(request):
    if request.method == "POST":
         form = BookForm(request.POST,request.FILES)
         if form.is_valid():
              form.save()
              return redirect('book_list')
    else:
         form = BookForm()
    return render(request, "upload_books.html",{"form":form})


@login_required # type: ignore
def delete_book(request,pk):
     if request.method == "POST":
          book = Upload_Book.objects.get(pk=pk)
          book.delete()
          return redirect('book_list')
     

########################################################

@login_required # type: ignore
def Active_Books(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ActiveBooks.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'qty', 'price','author', 'is_published','is_active'])

    get_book = Book.objects.all().filter(is_active = True)
    books = get_book.values_list('name', 'qty', 'price','author', 'is_published','is_active')
    for book in books:
        writer.writerow(book)

    return response


@login_required # type: ignore
def InActive_Books(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InActiveBooks.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'qty', 'price','author', 'is_published','is_active'])

    get_book = Book.objects.all().filter(is_active = False)
    books = get_book.values_list('name', 'qty', 'price','author', 'is_published','is_active')
    for book in books:
        writer.writerow(book)

    return response

import openpyxl
from django.http import HttpResponse


@login_required # type: ignore
def Multiple_Sheets(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=books.xlsx'
    wb = openpyxl.Workbook()

    # creating active books worksheet
    active_ws = wb.active
    active_ws.title = "Active Books" # type: ignore
    active_books = Book.objects.filter(is_active=True)

    # adding headers row
    active_ws.append(['name', 'qty', 'price','author', 'is_published','is_active']) # type: ignore

    # addinng data rows
    for book in active_books:
        active_ws.append([book.name, book.qty, book.price, book.author, book.is_published,book.is_active]) # type: ignore

    # creating inactive books worksheet
    inactive_ws = wb.create_sheet("Inactive Books")

    # adding header row
    inactive_ws.append(['name', 'qty', 'price','author', 'is_published','is_active'])

    # adding data rows
    inactive_books = Book.objects.filter(is_active=False)
    for book in inactive_books:
        inactive_ws.append([book.name, book.qty, book.price, book.author, book.is_published,book.is_active])

    wb.save(response) # type: ignore
    return response








#using raw queries

import csv
from django.db import connection





@login_required # type: ignore
def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rawbook.csv"'
    writer = csv.writer(response)
    # Writing header 
    writer.writerow(['name', 'qty', 'price','author','is_published','is_active'])
    
#     queryset = Book.objects.all()
#     for obj in queryset:
#         writer.writerow([obj.name, obj.qty, obj.price,obj.author,obj.is_published,obj.is_active])
#     return response

    with connection.cursor() as cursor:
        cursor.execute("SELECT name, qty, price, author, is_published, is_active FROM April.Book;")
        rows = cursor.fetchall()
    for row in rows:
        writer.writerow(row)
    return response