# exec(open(r'E:\vspython\B8_django\april_LIBRARY\App1\db_shell.py').read())

from App1.models import Book

from django.contrib.auth.models import User

# print(User.objects.all())

# print(Book.objects.filter(name= "S"))
# print(Book.objects.all())


# obj = Book.objects.get(id= "4")
# print(obj)
# obj.name = "ironman"
# print(obj)
# obj.save()
# print(obj)

# updating existing database values
# for i in range(25):
#      obj = Book.objects.filter(id= i).update(price = 100 + 0.5*(i))
# print(obj)

# for i in range(25):
#      obj = Book.objects.filter(id= i).update(qty = 100 + i**2 )
# print(obj)


#raw queries

from django.db import connection
cursor = connection.cursor()

cursor.execute('select * from april.Book')
# print(cursor.fetchall())
# print(cursor.fetchmany(4))
# print(cursor.fetchmany(2))

