from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,CreateView,View,ListView
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


#auth_decorator

def sign_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect('login')

    return inner

dec=[sign_required,never_cache]


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
                    return redirect('admin')  
                
                else:
                    return redirect('home') 
            else:
                return render(request, 'login.html', {'form': form_data})
            

class LogOut(View):
    def get(self,request):
        logout(request)
        return redirect('login')
            

class Registration(CreateView):
    template_name='registration.html'
    form_class=RegistraionForm
    success_url=reverse_lazy('login')



# class HomePage(View):
#     def get(self,request):
#         form=Details()
#         return render(request,'home.html',{'form':form})
#     def post(self,request):
#         form_data=Details(data=request.POST)
#         if form_data.is_valid:
#             return redirect('resort')
#         else:
#             return render(request,'home.html',{'form':form_data})




@method_decorator(dec,name='dispatch')
class HomePage(View):
    def get(self,request):
        form=Details()
        return render(request,'home.html',{'form':form})
    def post(self,request):
                form = Details(request.POST)
                if form.is_valid():
                    check_in = form.cleaned_data['CheckIn']
                    check_out = form.cleaned_data['CheckOut']
                    adults = form.cleaned_data['Adults']
                    kids = form.cleaned_data['Kids']

                    # Create a new Customer object and save it to the database
                    # customer = Customer(
                    #     CheckIn=check_in,
                    #     CheckOut=check_out,
                    #     Adults=adults,
                    #     Kids=kids
                    # )
                    # book=customer.save()
                    book={"cin":str(check_in),"cout":str(check_out),"ad":adults,"kids":kids}
                    print(book)
                    request.session['book']=book

                    # Render a success message or redirect to a success page
                    return redirect('resort')

                else:
                    form = Details()

                    return render(request, 'home.html', {'form': form})



@method_decorator(dec,name='dispatch')
class ResortView(ListView):
    template_name='resorts.html'
    model=Resort
    context_object_name='data'
    

@method_decorator(dec,name='dispatch')
class BookedView(ListView):
    template_name='booked.html'
    model=Customer
    context_object_name='data'
    def get_queryset(self):
        return Customer.objects.filter(Email=self.request.user.email)


@method_decorator(dec,name='dispatch')
class Payment(TemplateView):
    template_name='payment.html'
    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        resort=Resort.objects.get(id=id)
        book=request.session['book']
        print(book)
        hotel=resort.name
        price=resort.price
        place=resort.place
        name=request.POST.get('Name')
        address=request.POST.get('Address')
        email=request.POST.get('Email')
        Customer.objects.create(CheckIn=book['cin'],CheckOut=book['cout'],Adults=book['ad'],Kids=book['kids'],Name=name,Address=address,Email=email,Resort_name=hotel,Resort_price=price,Resort_place=place)
        resort.save()
        messages.success(request,'Resort Booked!!')
        return redirect('home')
    

dec
def filter(request):
    products=Resort.objects.order_by('price')
    return render(request, 'filter.html', {'products': products})


dec
def filter_2(request):
    product=Resort.objects.order_by('-price')
    return render(request,'filter_2.html',{"products":product})


@method_decorator(dec,name='dispatch')
class Admin(ListView):
    template_name ='admin.html'
    model=Customer
    context_object_name='data'


    def product_list(request):
        data = Customer.objects.all()
        return render(request, 'admin.html', {'data': data})


@method_decorator(dec,name='dispatch')
class AdminLogout(View):
    def get(self,request):
        logout(request)
        return redirect('login')