from django.shortcuts import render,redirect
import datetime
from django.http import HttpResponse, Http404,JsonResponse, HttpResponseRedirect
from salikneta.models import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
import datetime
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
            request.session['userID'] = Cashier.objects.get(username=user, password=password).idCashier
            return render(request, 'salikneta/home.html')
        elif try2: 
            request.session['username'] = user
            request.session['usertype'] = "manager"
            request.session['logged'] = True

            request.session['userID'] = Manager.objects.get(username=user, password=password).idManager
            return render(request, 'salikneta/home.html')
        else:
            messages.warning(request, 'Wrong credentials, please try again.')
   
    return render(request, 'salikneta/login.html')
def home(request):
    return render(request, 'salikneta/home.html')

def pos(request):
    if request.method == 'POST':
        #create Sales invoice
        si = SalesInvoice(invoiceDate=datetime.datetime.now(),
                          customer="WALK-IN",
                          idCashier_id=1)# will replace to request.session['userID']

        ils =[]
        itms = []
        itms_dict ={}
        pazucc = True
        items = request.POST.getlist('prod_codes[]')
        qtys = request.POST.getlist('qty[]')
        discs = request.POST.getlist('disc[]')

        for i,item in enumerate(items,0):
            if item not in itms:
                itms.append(item)
                itms_dict[item]=0
            prod = Product.objects.get(idProduct=item)
            il = InvoiceLines(qty=float(qtys[0]),
                              unitPrice=prod.suggestedUnitPrice*float(qtys[0]),
                              disc=float(discs[0]),
                              idProduct_id=item
                              )
            itms_dict[item] += float(qtys[0])
            ils.append(il)
        for i in itms_dict:
            prod = Product.objects.get(idProduct=i)
            if prod.unitsInStock - itms_dict[i] < 0:
                pazucc = False
        if pazucc:
            '''
            for i in itms_dict:
                prod = Product.objects.get(idProduct=i)
                prod.unitsInStock = prod.unitsInStock - itms_dict[i]
            '''
            si.save()
            for i in ils:
                i.idSales = si
                i.save()
        return HttpResponseRedirect(reverse('pos'))
        #loop the arrays
    return render(request, 'salikneta/pos/pos.html',{'products': Product.objects.all(),
                                                     'si_num':SalesInvoice.get_latest_invoice_num(),
                                                     'date':datetime.datetime.now(),
                                                     'categories':Category.objects.all()})
def signout(request):
    return redirect('index')
def purchaseOrder(request):
    s = Supplier.objects.all()
    usertype = request.session['usertype']
    if usertype == "manager":
        m = Manager.objects.filter(username=request.session['username']).select_related("idBranch")
        branch = m[0].idBranch.name
    if usertype == "cashier":
        m = Cashier.objects.filter(username=request.session['username']).select_related("idBranch")
        branch = m[0].idBranch.name

    i = Product.objects.all()
    purchaseOrders = PurchaseOrder.objects.filter().select_related("idSupplier")


    context = {
        "suppliers":s,"branch":branch,"products":i,"purchaseOrders":purchaseOrders,
    }
    return render(request, 'salikneta/purchaseOrder.html',context)

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
    c = Category.objects.all()
    i = Product.objects.all()

    context = {
        "categories":c,
        "products":i,
    }
    if request.method == 'POST':
        c = Product(name=request.POST['itemName'], description=request.POST['description'],
                    suggestedUnitPrice=request.POST['price'], unitsInStock=request.POST['startStock'],
                    img_path=request.FILES['image'], reorderLevel=request.POST['reorder'], unitOfMeasure=request.POST['unitsOfMeasure'],
                    SKU=request.POST['SKU'],idCategory_id=request.POST['category'])
        c.save()
        return HttpResponseRedirect(reverse('manageItems'))
    return render(request, 'salikneta/manageItems.html',context)

def backload(request):

    return render(request, 'salikneta/backloads.html')

def ajaxAddCategory(request):
    print("AW")
    name = request.GET.get('categoryName')
    desc = request.GET.get('description')
    print("WEW")
    c = Category(name=name,description=desc)
    c.save()

    return HttpResponse()

def ajaxAddItem(request):
    print("AW")
    itemName = request.GET.get('itemName')
    category = request.GET.get('category')
    price = request.GET.get('price')
    SKU = request.GET.get('SKU')
    reorder = request.GET.get('reorder')
    unitsOfMeasure = request.GET.get('unitsOfMeasure')
    description = request.GET.get('description')
    print("WEW")
    c = Product(name=itemName,description=description, suggestedUnitPrice=price, unitsInStock=0,img_path=request.FILES['image'], reorderLevel=reorder,unitOfMeasure=unitsOfMeasure,SKU=SKU,idCategory_id = category)
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

def ajaxGetUpdatedItems(request):
    print("Waa2aaaE")
    c = Product.objects.all()
    products = []
    for x in range(0, len(c)):
        products.append({"name":c[x].name,"category":c[x].idCategory.name,"price":c[x].suggestedUnitPrice,"SKU":c[x].SKU,"reorder":c[x].reorderLevel})
        



    return JsonResponse(products, safe=False)


def ajaxGetInStock(request):

    pk = request.GET.get('idProduct')
    c = Product.objects.get(pk=pk)
    products = []

    products.append({"idProduct":c.pk,"unitsInStock":c.unitsInStock,"incoming":c.get_num_incoming})
        



    return JsonResponse(products, safe=False)

def ajaxAddPurchaseOrder(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    supplier = request.GET.get('supplier')
    shipTo = request.GET.get('shipTo')
    orderDate = request.GET.get('orderDate')
    expectedDate = request.GET.get('expectedDate')


    po = PurchaseOrder(orderDate=datetime.datetime.strptime(orderDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    ,expectedDate=datetime.datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    , idCashier_id=request.session['userID'], idSupplier_id = supplier,status="In Transit")
    po.save()


    for x in range(0, len(products)):
        orderLine = OrderLines(qty=quantity[x],idProduct_id=products[x],idPurchaseOrder_id=po.pk)
        orderLine.save()

    return HttpResponse()