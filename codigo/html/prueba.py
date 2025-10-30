# prueba.py
import django
print(django.get_version())


from django.http import HttpResponse
def homepage(request):
 return HttpResponse("Hello World!")
