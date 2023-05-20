from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from assets.models import *
#from accounts.models import User
from .forms import AssetForm, VendorForm, UserForm, SuperUserForm
#from django.db.models import F

from django.views.generic.edit import FormView

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.
from django.contrib.auth.decorators import login_required 

from .decorators import unauthenticated_user, allowed_users, admin_only, super_user

# for date and time 
from datetime import datetime

#for vendor countries 
from django.db.models import Count

#filters
from .filters import AssetFilter, AssetFilter_User


def index(request):
	context = {}
	return render(request, 'app/index.html', context)


#from django.utils.text import force_text

@login_required(login_url='login')
@admin_only
def home(request):

    total_asset = Assets.objects.count()
    total_emp = Employee.objects.count()
    dept   = Assign.objects.count()
    total_vendor = Vendor.objects.count()
    
     #for assets display 

    New_Assets = Assets.objects.filter(Asset_State = 'New')
    Good_Assets = Assets.objects.filter(Asset_State = 'Good')
    Used_Assets = Assets.objects.filter(Asset_State = 'Used')
    Defective_Assets = Assets.objects.filter(Asset_State = 'Defective')

    #Asset Vendors by country 
    # Render some queries here 
    qs = Vendor.objects.values('Country').annotate(
        number=Count('pk')
    ).order_by('Country')
    result = {q['Country']: q['number']for q in qs}


    ##Render User Activity ####
    employee = Employee.objects.all() #

    assets_by_employee = Assets.objects.all().order_by('Employee').values('Employee').annotate(asset_count=Count('id'))

    assets_by_employees = Assets.objects.all().prefetch_related('Employee').annotate(asset_count=Count('id')).order_by('Employee__Full_Name')


    myquery = {
        "total_asset" : total_asset,
        "total_emp" : total_emp,
        "dept"   : dept,
        "total_vendor": total_vendor,

        #for assets display 

        "New_Assets" : New_Assets,
        "Good_Assets" : Good_Assets,
        "Used_Assets" : Used_Assets,
        "Defective_Assets" : Defective_Assets,

        #Asset Vendors by country 
        "result": result,

        #EMployee to be rendered 
        "employee" : employee,

        "assets_by_employee":assets_by_employee,

        "assets_by_employees":assets_by_employees,
        
    }

    return render(request, 'home.html', myquery )

@login_required(login_url='login')
def table(request):
   
    vendor = Vendor.objects.all()

    assets = Assets.objects.all()

    myFilter = AssetFilter(request.GET, queryset=assets)
    assets = myFilter.qs

    UserFilterAsset = AssetFilter_User(request.GET, queryset=assets)
    assets = UserFilterAsset.qs
    #tblquery = myFilter.qs # filter later

    tblquery = {
        "vendor" : vendor,
        "assets" : assets,
        'myFilter' : myFilter,
        'UserFilterAsset': UserFilterAsset,

    }
   

    return render(request, 'table.html', tblquery)


@login_required(login_url='login')
def registerassets(request):

    Assetform = AssetForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Assetform = AssetForm(request.POST)
       if Assetform.is_valid(): 
        Assetform.save()
        messages.success(request, 'Asset has been successfully added.')
        return redirect('registerassets')

    Vendorform = VendorForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Vendorform = VendorForm(request.POST)
       if Vendorform.is_valid(): 
        Vendorform.save()
        messages.success(request, 'Vendor has been successfully added.')
        return redirect('registerassets')

    context = {'Assetform': Assetform,'Vendorform': VendorForm }
    return render(request, 'registerassets.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def userPage(request):
    
    asset = request.user.employee.assets_set.all()

    assetInCharge = request.user.employee.assets_set.all().count()

    Emp_New_Assets = request.user.employee.assets_set.filter(Asset_State = 'New').count() 
    Emp_Good_Assets = request.user.employee.assets_set.filter(Asset_State = 'Good').count() 
    Emp_Used_Assets = request.user.employee.assets_set.filter(Asset_State = 'Used').count() 
    Emp_Defective_Assets = request.user.employee.assets_set.filter(Asset_State = 'Defective').count() 


    #assetw = request.user.employee.assets.quantity_set.all() to be done later 
    total_asset = asset.count()

    #total_quantity = assetw.count()
    
    context = {'asset':asset, 'total_asset':total_asset, 'assetInCharge':assetInCharge, 
    'Emp_New_Assets':Emp_New_Assets,'Emp_Good_Assets':Emp_Good_Assets,
    'Emp_Used_Assets':Emp_Used_Assets,'Emp_Defective_Assets':Emp_Defective_Assets}
    return render(request, 'users.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def accountSettings(request):
    employee = request.user.employee
    form = UserForm(instance=employee)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=employee)
        if form.is_valid():
            form.save()

            
    context = {'form':form}
    return render(request, 'account_settings.html', context)

##################### User Details Page ###########################

@login_required(login_url='login')
#@allowed_users(allowed_roles=['users'])
@super_user(allowed_roles=['super_admin'])
def userDetails(request, employee_id=None):

    #employee = Employee.objects.get(id=employee_id)
    #asset_count = Assets.objects.filter(employee=employee).count()

    if employee_id is not None:
        employee = Employee.objects.get(id=employee_id)
        asset_count = Assets.objects.filter(employee=employee).count()
    else:
        employee = None
        asset_count = 0
   
    context = {'employee': employee, 'asset_count': asset_count}
    return render(request, 'userdetails.html', context)
    


@login_required(login_url='login')
@super_user(allowed_roles=['super_admin'])
def accountSuperSettings(request):
    super = request.user
    form = SuperUserForm(instance=super)

    if request.method == 'POST':
        form = SuperUserForm(request.POST, request.FILES,instance=super)
        if form.is_valid():
            form.save()

            
    context = {'form':form}
    return render(request, 'account_settings.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email or Password is Incorrect')

    context = {}
    return render(request, 'registration/login.html')

#@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
#def updateAsset(request, pk):

#    asset = Assets.objects.get(id=pk)
#    Assetform = AssetForm(instance=asset)
    
#    if request.method == 'POST':
#       Assetform = AssetForm(request.POST, instance=asset)
#       if Assetform.is_valid(): 
#        Assetform.save()
#        return redirect('table')

#    context = {'Assetform':Assetform}
#    return render(request, 'asset_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','users'])
def asset_update(request, pk):

    asset = get_object_or_404(Assets, pk=pk)

    form = AssetForm(instance=asset)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Asset {asset.Name} was updated successfully')
            return redirect('table')
        
    return render(request, 'asset_form.html', {'form': form, 'title':'Update Asset', 'method':'PUT'})



#@login_required(login_url='login')
#def updateVendor(request, pk):

 #   vendor = Vendor.objects.get(id=pk)
  #  Vendorform = VendorForm(instance=vendor)
    
   # if request.method == 'POST':
    #   Vendorform = VendorForm(request.POST, instance=vendor)
     #  if Vendorform.is_valid(): 
      ##  Vendorform.save()
        #return redirect('registerassets')

#    context = {'Vendorform': Vendorform}
 #   return render(request, 'registerassets.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAsset(request, pk):

    asset = Assets.objects.get(id=pk)
    if request.method == "POST":
        asset.delete()
        return redirect('/')

    context = {'item':asset}
    return render(request, 'delete.html', context)

#Show the date and time of a record 
def showdate(request):
    datetime.datetime.now()
    return render(request, 'home.html')


#employee report 
def employeeReport(request):
    employee_list = Employee.objects.all()
    return render(request, 'report/employeereport.html', {'employee_list': employee_list})

#vendor report 
def vendorReport(request):
    vendor_list = Vendor.objects.all()
    return render(request, 'report/vendorreport.html', {'vendor_list': vendor_list})

#asset report 
def assetReport(request):
    asset_list = Assets.objects.all()
    return render(request, 'report/assetreport.html', {'asset_list': asset_list})