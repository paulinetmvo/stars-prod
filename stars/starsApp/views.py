from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from .forms import UserForm
from .models import Contact

from django.views.generic import FormView, TemplateView
from .forms import ContactForm
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, 'index.html')

def imprint(request):
    return render(request, 'impressum.html')

def user(request):
    return render(request, 'nutzer.html')

def reservations(request):
    return render(request, 'reservierungen.html')

#def support(request):
     #if request.method == "POST":
      #      contact = Contact()
       #     contact.name = request.POST['name']
         #   contact.subject = request.POST['subject']
        #    from_email= request.POST['email']
          #  message = request.POST['message']
          #  contact.save()
           # return HttpResponse("<h1 style = font-family:Verdana> Thanks, your message was successfully submitted.</h1>")
     #else:
      #  return render(request, 'support.html')


def support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            return HttpResponse("<h1> Die Anfrage wurde erfolgreich versendet!</h1>")
    else:
        form = ContactForm()
    return render(request, 'support.html', {'form': form})


    
def arbeitsplaetze(request):
    return render(request, 'arbeitsplaetze.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registrieren.html', {'form': form})

def login(request):
    return render(request, 'login.html')
