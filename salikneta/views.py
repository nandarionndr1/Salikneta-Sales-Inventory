from django.shortcuts import render,redirect

from django.http import HttpResponse, Http404,JsonResponse
from salikneta.models import * 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'salikneta/login.html')
def log_in(request):
    return render(request, 'salikneta/login.html')
def log_in_validate(request):
    if request.method == "POST":

        user = request.POST.get('user')
        password = request.POST.get('password')
        try1 = Cashier.objects.filter(username=user, password=password).exists()
        try2 = Manager.objects.filter(username=user, password=password).exists()
        if try1:
            request.session['username'] = user
            request.session['usertype'] = "cashier"
            request.session['logged'] = True
            return render(request, 'salikneta/home.html')
        elif try2: 
            request.session['username'] = user
            request.session['usertype'] = "manager"
            request.session['logged'] = True
            return render(request, 'salikneta/home.html')
        else:
            messages.warning(request, 'Wrong credentials, please try again.')
   
    return render(request, 'salikneta/login.html')
def home(request):
    return render(request, 'salikneta/home.html')

def pos(request):
    return render(request, 'salikneta/pos/pos.html')
def signout(request):
    return redirect('index')
def register(request):
    branches = Branch.objects.all()
    context = {
        "branches":branches
    }
    return render(request, 'salikneta/register.html',context)
def register_validate(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        usertype = request.POST.get('usertype')
        branch = request.POST.get('branch')
        print(branch)
        print(usertype)
        if usertype == "manager":
            manager = Manager(firstname = fname, lastname = lname, username=username,password=password, idBranch_id=branch)
            manager.save()
        if usertype == "cashier":
            cashier = Cashier(firstname = fname, lastname = lname, username=username,password=password, idBranch_id=branch)
            cashier.save()
        print("done")



        # if usertype == "os":
        #     group = Group.objects.get(name="Operations Supervisor")
        #     user.groups.add(group)
        # elif usertype == "gk":
        #     group = Group.objects.get(name="Gamekeeper")
        #     user.groups.add(group)
        # elif usertype == "own":
        #     group = Group.objects.get(name="Owner")
        #     user.groups.add(group)

        # user.save()
        messages.warning(request, 'Account Created.')
        return render(request, 'salikneta/login.html')
    return render(request, 'salikneta/register.html')

def manageCategories(request):
    c = Category.objects.all()
    context = {
        "categories":c,
    }

    return render(request, 'salikneta/manageCategories.html',context)

def manageSuppliers(request):
    s = Supplier.objects.all()
    context = {
        "suppliers":s,
    }
    return render(request, 'salikneta/manageSuppliers.html',context)

def manageItems(request):
    return render(request, 'salikneta/manageItems.html')

def ajaxAddCategory(request):
    print("AW")
    name = request.GET.get('categoryName')
    desc = request.GET.get('description')
    print("WEW")
    c = Category(name=name,description=desc)
    c.save()

    return HttpResponse()

def ajaxAddSupplier(request):
    supplierName = request.GET.get('supplierName')
    contactNumber = request.GET.get('contactNumber')
    emailAddress = request.GET.get('emailAddress')
    website = request.GET.get('website')
    address1 = request.GET.get('address1')
    address2 = request.GET.get('address2')
    city = request.GET.get('city')
    province = request.GET.get('province')
    country = request.GET.get('country')
    postal = request.GET.get('postal')

    s = Supplier(name=supplierName, contactNumber=contactNumber, emailAddress=emailAddress, website=website, address1=address1, address2=address2, city=city,province=province,
        country=country,postal=postal)
    s.save()

    return HttpResponse()


def ajaxGetUpdatedCategories(request):
    print("WaaaaaE")
    c = Category.objects.all()
    categories = []
    for x in range(0, len(c)):
        categories.append({"name":c[x].name,"description":c[x].description})


    return JsonResponse(categories, safe=False)

def ajaxGetUpdatedSuppliers(request):
    print("Waa2aaaE")
    c = Supplier.objects.all()
    suppliers = []
    for x in range(0, len(c)):
        suppliers.append({"name":c[x].name,"contactNumber":c[x].contactNumber,"emailAddress":c[x].emailAddress, "address1":c[x].address1, "city":c[x].city,"country":c[x].country})



    return JsonResponse(suppliers, safe=False)