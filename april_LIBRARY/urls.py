"""april_LIBRARY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users import views as user_view
from App1 import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),


    path("welcome/" ,views.home, name="home"),   # type: ignore
    path('show_book/',views.show_books , name="active_books"),
    path('inactive_books/',views.show_inactive_books , name="inactive_books"),

    path('recover-book/<int:pk>',views.recover_book , name="recover_book"),

    path('update-book/<int:pk>',views.update_book , name="update_book"),
    path('delete/<int:pk>',views.hard_delete , name="hard_delete"),
    path('soft-delete/<int:pk>',views.soft_delete , name="soft_delete"),

    path('create-csv/',views.create_csv , name="create_csv"),
    path('upload-csv/',views.upload_csv , name="upload_csv"),

    path("Active-books/", views.Active_Books, name="Active_Books"),
    path("Inactive-books/", views.InActive_Books, name="InActive_Books"),
    path('Multiple-Sheets/', views.Multiple_Sheets, name='Multiple_Sheets'),


     path('sample-csv/', views.download_csv, name='sample_csv'),








    # simple upload
    path("upload/" ,views.upload, name="upload"), 


    path("register/", user_view.register_request, name="register"),
    path("login/", user_view.login_request, name="login"),
    path("logout/", user_view.logout_request, name= "logout_user"),

    # ## function based view upload and download
    path('book-list/',views.book_list,name='book_list'),
    path('books/upload/',views.upload_books,name='upload_books'),
    path('books/<int:pk>/',views.delete_book,name='delete_book'),  # type: ignore

    
    
    path('export/', views.export_data, name='export_data'),


    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

