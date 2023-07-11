from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,CreateView,View,ListView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

class LoginPage(FormView):
    template_name='login.html'
    form_class=LoginForm
    def post(self,request):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            username=form_data.cleaned_data.get('username')
            password=form_data.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin')  # Redirect to admin page
                else:
                    return redirect('home')  # Redirect to home page
            else:
                return render(request, 'login.html', {'form': form_data})



class Registration(CreateView):
    template_name='registration.html'
    form_class=RegistraionForm
    success_url=reverse_lazy('login')



class HomePage(View):
    def get(self,request):
        form=CheckIn()
        return render(request,'home.html',{'form':form})
    def post(self,request):
        form_data=CheckIn(data=request.POST)
        if form_data.is_valid:
            return redirect('resort')
        else:
            return render(request,'home.html',{'form':form_data})




class ResortView(ListView):
    template_name='resorts.html'
    model=Resort
    context_object_name='data'
    



class Payment(TemplateView):
    template_name='payment.html'
    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        resort=Resort.objects.get(id=id)
        hotel=resort.name
        price=resort.price
        place=resort.place
        name=request.POST.get('Name')
        address=request.POST.get('Address')
        email=request.POST.get('Email')
        Customer.objects.create(Name=name,Address=address,Email=email,Resort_name=hotel,Resort_price=price,Resort_place=place)
        resort.save()
        messages.success(request,'Resort Booked!!')
        return redirect('home')
    


def filter(request):
    products=Resort.objects.order_by('price')
    return render(request, 'filter.html', {'products': products})



def filter_2(request):
    product=Resort.objects.order_by('-price')
    return render(request,'filter_2.html',{"products":product})


class Admin(ListView):
    template_name ='admin.html'
    model=Customer
    context_object_name='data'

    def product_list(request):
        data = Customer.objects.all()
        return render(request, 'admin.html', {'data': data})