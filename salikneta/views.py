from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,JsonResponse, HttpResponseRedirect
from salikneta.models import *
from django.urls import reverse
from django.contrib import messages
import calendar
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from datetime import datetime,timedelta
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
            request.session['firstname'] = Cashier.objects.get(username=user, password=password).firstname
            request.session['lastname'] = Cashier.objects.get(username=user, password=password).lastname
            return redirect('home')
        elif try2: 
            request.session['username'] = user
            request.session['usertype'] = "manager"
            request.session['logged'] = True

            request.session['userID'] = Manager.objects.get(username=user, password=password).idManager
            request.session['firstname'] = Manager.objects.get(username=user, password=password).firstname
            request.session['lastname'] = Manager.objects.get(username=user, password=password).lastname
            return redirect('home')
        else:
            messages.warning(request, 'Wrong credentials, please try again.')
   
    return render(request, 'salikneta/login.html')
def home(request):
    return render(request, 'salikneta/home.html',{"notifs":Notifs.objects.all()})

def get_num_lowstock(request):
    return JsonResponse({"numb":Product.get_num_lowstock_items()})

def get_invoice_by_id(request, idSales):
    data = []
    for il in SalesInvoice.objects.get(idSales=idSales).get_invoicelines:
        data.append({"unitPrice":il.unitPrice,
                     "qty":il.qty,
                     "disc":il.disc,
                     "net_price":il.get_net_price,
                     "productName":il.idProduct.name,
                     "uom":il.idProduct.unitOfMeasure})
    return JsonResponse({"data":data})
def sales(request):
    return render(request, 'salikneta/sales.html',{"sales_invoices":SalesInvoice.objects.all()})

def sales_report(request):
    return render(request, 'salikneta/reports/sales_report.html')
def sales_report_detail(request):
    if request.method == 'POST':
        report_data = []
        new_rd = []
        gen_info ={"message":"","total_qty":0,"total_sales":0}
        products = Product.objects.all()
        for p in products:
            report_data.append({"id":p.idProduct,
                                "product": p.name,
                                "description":p.description,
                                "total_qty":0,
                                "total_value":0,
                                "sold_value":0})
        if request.POST['type'] == "range":
            sd = request.POST["sd"].split("/")[2]+"-"+request.POST["sd"].split("/")[0]+"-"+request.POST["sd"].split("/")[1] + " 00:00:00"
            ed = request.POST["ed"].split("/")[2]+"-"+request.POST["ed"].split("/")[0]+"-"+request.POST["ed"].split("/")[1] + " 00:00:00"
            gen_info["message"] = "From "+sd+" to "+ed
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            for r in report_data:
                for s in si:
                    for il in s.get_invoicelines:
                        if r["id"] == il.idProduct_id:
                            r["total_qty"] += il.qty
                            r["total_value"] += il.unitPrice * il.qty
                            r["sold_value"] += il.get_net_price

                            gen_info["total_sales"]+= il.get_net_price
                            gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
        elif request.POST['type'] == "month":
            print(request.POST["month"])
            m = request.POST["month"].split("-")[1]+"-"+request.POST["month"].split("-")[0]+"-01 00:00:00"
            m = datetime.strptime(m , '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__year=m.year)
            gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
            for r in report_data:
                for s in si:
                    if m.month == s.invoiceDate.month:
                        for il in s.get_invoicelines:
                            if r["id"] == il.idProduct_id:
                                r["total_qty"] += il.qty
                                r["total_value"] += il.unitPrice * il.qty
                                r["sold_value"] += il.get_net_price
                                gen_info["total_sales"]+= il.get_net_price
                                gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
        elif request.POST['type'] == "day":
            sd = request.POST["date"].split("-")[2]+"-"+request.POST["date"].split("-")[0]+"-"+request.POST["date"].split("-")[1] + " 00:00:00"
            ed = request.POST["date"].split("-")[2] + "-" + request.POST["date"].split("-")[0] + "-" + request.POST["date"].split("-")[1] + " 23:59:59"
            gen_info["message"] = "For "+request.POST["date"]
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            for r in report_data:
                for s in si:
                    for il in s.get_invoicelines:
                        if r["id"] == il.idProduct_id:
                            r["total_qty"] += il.qty
                            r["total_value"] += il.unitPrice * il.qty
                            r["sold_value"] += il.get_net_price

                            gen_info["total_sales"]+= il.get_net_price
                            gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
    else:
        return redirect('sales_report')
    return render(request, 'salikneta/reports/sales_report_detail.html',{"report_data":new_rd,"gen_info":gen_info})

def inventory_report(request):
    return render(request, 'salikneta/reports/inventory_report.html')

def inventory_report_detail(request):
    if request.method == 'POST':
        report_data = []
        gen_info ={"message":"","total_sales_ct":0,
                   "total_deliveries":0,
                   "total_backloads":0,
                   "transfer_out": 0}
        products = Product.objects.all()
        for p in products:
            report_data.append({"id":p.idProduct,
                                "product": p.name,
                                "uom":p.unitOfMeasure,
                                "unit_price":p.suggestedUnitPrice,
                                "beg_inv":0,
                                "transfer_out":0,
                                "deliveries":0,
                                "returns":0,
                                "sales":0,
                                "end_inv":0})
        if request.POST['type'] == "range":
            sd = request.POST["sd"].split("/")[2]+"-"+request.POST["sd"].split("/")[0]+"-"+request.POST["sd"].split("/")[1] + " 00:00:00"
            ed = request.POST["ed"].split("/")[2]+"-"+request.POST["ed"].split("/")[0]+"-"+request.POST["ed"].split("/")[1] + " 00:00:00"
            gen_info["message"] = "From "+sd+" to "+ed
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')

            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
            deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)
            to = TransferOrder.objects.filter(transferDate__gte=sd, transferDate__lte=ed)
            for r in report_data:
                sl = 0
                backloads = 0
                deliveries = 0
                tos = 0
                r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed)
                for d in deliv:
                    for del_prods in d.get_delivered_products:
                        if del_prods.product.idProduct == r["id"]:
                            deliveries += del_prods.qty
                            gen_info["total_deliveries"] += del_prods.qty
                for s in si:
                    for il in InvoiceLines.objects.filter(idSales=s, idProduct_id=r["id"]):
                        sl += il.qty
                        gen_info["total_sales_ct"] += il.qty
                for b in bload:
                    for bl in BackloadLines.objects.filter(idBackload=b, idProduct_id=r["id"]):
                        backloads += bl.qty
                        gen_info["total_backloads"] += bl.qty
                for t in to:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_out"] += tl.qty
                            tos += tl.qty

                r["beg_inv"] = (r["end_inv"] + sl + backloads + tos) - deliveries
                r["deliveries"] = deliveries
                r["returns"] = backloads
                r["transfer_out"] = tos
                r["sales"] = sl

        elif request.POST['type'] == "month":
            m = request.POST["month"].split("-")[1]+"-"+request.POST["month"].split("-")[0]+"-01 00:00:00"
            m = datetime.strptime(m , '%Y-%m-%d %H:%M:%S')
            sd = request.POST["month"].split("-")[1]+"-"+request.POST["month"].split("-")[0]+"-01"
            ed = request.POST["month"].split("-")[1]+"-"+request.POST["month"].split("-")[0]+"-"+str(calendar.monthrange(m.year, m.month)[1])

            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
            deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)

            to = TransferOrder.objects.filter(transferDate__gte=sd, transferDate__lte=ed)
            gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
            for r in report_data:
                sl = 0
                backloads = 0
                deliveries = 0
                tos = 0
                r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed)
                for d in deliv:
                    for del_prods in d.get_delivered_products:
                        if del_prods.product.idProduct == r["id"]:
                            deliveries += del_prods.qty
                            gen_info["total_deliveries"] += del_prods.qty
                for t in to:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_out"] += tl.qty
                            tos += tl.qty

                for s in si:
                    for il in InvoiceLines.objects.filter(idSales=s):
                        if il.idProduct_id == r["id"]:
                            sl += il.qty
                            gen_info["total_sales_ct"] += il.qty
                for b in bload:
                    for bl in BackloadLines.objects.filter(idBackload=b):
                        if bl.idProduct_id == r["id"]:
                            backloads += bl.qty
                        gen_info["total_backloads"] += bl.qty

                r["beg_inv"] = (r["end_inv"] + sl + backloads + tos) - deliveries
                r["deliveries"] = deliveries
                r["returns"] = backloads
                r["transfer_out"] = tos
                r["sales"] = sl
    else:
        return redirect('inventory_report')
    return render(request, 'salikneta/reports/inventory_report_detail.html',{"report_data":report_data,"gen_info":gen_info})

def editItemPrice(request):
    if request.method == 'POST':
        print("waaat",request.POST['item_price'])
        print("waaat",request.POST['item_id'])
        p = Product.objects.get(idProduct=request.POST['item_id'])
        print("waaat",request.POST['item_price'])
        p.suggestedUnitPrice = float(request.POST['item_price'])
        p.save()
        Notifs.write("Price for " +p.name+" has been updated.")
    return HttpResponseRedirect(reverse('manageItems'))
def open_notif(request):
    notifs = Notifs.objects.all()
    for n in notifs:
        n.viewed = 1
        n.save()
    return JsonResponse({"data": 'ok'})
def check_notif(request):
    notifs = Notifs.objects.all().order_by("-timestamp")[0:5]
    chk = Notifs.check_num_new_notif()
    data=[]
    for n in notifs:
        data.append({"num_notif":chk,
                     "msg":n.msg
                        ,"timestamp":n.get_time_ago})
    return JsonResponse({"data": data})

def pos(request):
    if request.method == 'POST':
        #create Sales invoice
        si = SalesInvoice(invoiceDate=datetime.now(),
                          customer="WALK-IN",
                          idCashier_id=request.session['userID'])# will replace to request.session['userID']
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
            il = InvoiceLines(qty=float(qtys[i]),
                              unitPrice=prod.suggestedUnitPrice,
                              disc=float(discs[i]),
                              idProduct_id=item
                              )
            itms_dict[item] += float(qtys[i])
            ils.append(il)
        for i in itms_dict:
            prod = Product.objects.get(idProduct=i)
            if prod.unitsInStock - itms_dict[i] < 0:
                pazucc = False
                messages.warning(request, 'Account Created.')
        if pazucc:
            for i in itms_dict:
                prod = Product.objects.get(idProduct=i)
                prod.unitsInStock = prod.unitsInStock - itms_dict[i]
                prod.save()
            si.save()
            for i in ils:
                i.idSales = si
                i.save()
        return HttpResponseRedirect(reverse('pos'))
        #loop the arrays
    return render(request, 'salikneta/pos/pos.html',{'products': Product.objects.all(),
                                                     'si_num':SalesInvoice.get_latest_invoice_num(),
                                                     'date':datetime.now(),
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
                    img_path=request.FILES['image'], reorderLevel=request.POST['reorder'],unitOfMeasure=request.POST['unitsOfMeasure'],
                    SKU=request.POST['SKU'],idCategory_id=request.POST['category'])
        c.save()

        Notifs.write("New Item -" +c.name+"- has been added.")
        return HttpResponseRedirect(reverse('manageItems'))
    return render(request, 'salikneta/manageItems.html',context)

def backload(request):

    b = BackLoad.objects.all()

    i = Product.objects.all()
    context = {
        "products":i,"backloads":b,
    }
    return render(request, 'salikneta/backloads.html',context)

def transferOrder(request):

    idUser = request.session['userID']
    usertype = request.session['usertype']

    if usertype == "cashier":
        c = Cashier.objects.filter(pk=idUser).select_related('idBranch')
        source = c[0].idBranch
    if usertype == "manager":
        c = Manager.objects.filter(pk=idUser).select_related('idBranch')
        source = c[0].idBranch

    destination = Branch.objects.filter(~Q(pk=source.pk))

    p = Product.objects.all()

    to = TransferOrder.objects.all()

    context = {
        "source":source,
        "destination":destination,
        "products":p,
        "transferOrders":to,
    }




    return render(request, 'salikneta/transferOrder.html',context)

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


    po = PurchaseOrder(orderDate=datetime.strptime(orderDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    ,expectedDate=datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    , idCashier_id=request.session['userID'], idSupplier_id = supplier,status="In Transit")
    po.save()


    for x in range(0, len(products)):
        orderLine = OrderLines(qty=quantity[x],idProduct_id=products[x],idPurchaseOrder_id=po.pk)
        orderLine.save()

    Notifs.write("New PO" + str(po.pk) + " has been added.")
    print("Success")

    return JsonResponse([], safe=False)

def ajaxAddBackload(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    reasons = request.GET.getlist('reasons[]')

    backloadDate = datetime.now().strftime("%Y-%m-%d")
    b = BackLoad(backloadDate=backloadDate,idCashier_id=request.session['userID'])
    b.save()

    for x in range(0, len(products)):
        b1 = BackloadLines(qty=quantity[x],idProduct_id=products[x],reason=reasons[x],idBackload_id=b.pk)
        b1.save()
        p = Product.objects.get(pk=products[x])
        print(p.unitsInStock)
        p.unitsInStock = p.unitsInStock - int(quantity[x]);
        print(p.unitsInStock)
        p.save()

    Notifs.write("Products have been backloaded.")
    # po = PurchaseOrder(orderDate=datetime.datetime.strptime(orderDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    # ,expectedDate=datetime.datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    # , idCashier_id=request.session['userID'], idSupplier_id = supplier,status="In Transit")
    # po.save()


    # for x in range(0, len(products)):
    #     orderLine = OrderLines(qty=quantity[x],idProduct_id=products[x],idPurchaseOrder_id=po.pk)
    #     orderLine.save()

    return JsonResponse([],safe=False)

def ajaxSaveDelivery(request):
    print("WEW")
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    ordered = request.GET.getlist('ordered[]')
    lines = request.GET.getlist('lines[]')
    idPurchaseOrder = request.GET.get('idPurchaseOrder')

    deliveryDate =datetime.now().strftime("%Y-%m-%d")

    d = Delivery(deliveryDate=deliveryDate,idPurchaseOrder_id=idPurchaseOrder)
    d.save()

    isOkay = True
    print(len(ordered))
    print(len(quantity))
    print(len(products))
    for x in range(0, len(products)):


        d1 = DeliveredProducts(qty=quantity[x],idDelivery_id=d.pk,idOrderLines_id=lines[x])
        d1.save()
        p = Product.objects.get(pk=products[x])
        if float(ordered[x]) != float(quantity[x]):
            print(float(p.unitsInStock))
            print(float(quantity[x]))
            isOkay = False

        p.unitsInStock = int(p.unitsInStock) + int(quantity[x])
        p.save()


    qwe = PurchaseOrder.objects.get(pk=idPurchaseOrder)
    if isOkay == True:
        qwe.status = "RECEIVED"
        qwe.save()
    else:
        qwe.status = "PARTIALLY RECEIVED"
        qwe.save()

    return JsonResponse([],safe=False)


def ajaxTransferOrder(request):


    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    transferDate = request.GET.get('transferDate')
    expectedDate = request.GET.get('expectedDate')


    to = TransferOrder(transferDate=datetime.strptime(transferDate, '%d-%m-%Y').strftime('%Y-%m-%d'),expectedDate=datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d'),idCashier_id=request.session['userID'],source_id=source,destination_id=destination,status="Draft")
    to.save()


    for x in range(0, len(products)):
        tl = TransferLines(qty=quantity[x],idProduct_id=products[x],idTransferOrder_id=to.pk)
        tl.save()
        p = Product.objects.get(pk=products[x])
        p.unitsInStock = int(p.unitsInStock) - int(quantity[x])
        p.unitsReserved = int(p.unitsReserved) + int(quantity[x])
        p.save()

    Notifs.write("Products have been delivered.")
    return JsonResponse([],safe=False)

def ajaxInTransitTO(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrder.objects.get(pk=int(idTO))
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idProduct
        aw.unitsReserved = aw.unitsReserved - int(wew[x].qty)
        aw.save()

    to.status = "In Transit"
    to.save()
    return JsonResponse([],safe=False)

def ajaxFinishedTO(request):

    idTO = request.GET.get('idTransferOrder')
    to = TransferOrder.objects.get(pk=int(idTO))
    
    to.status = "Finished"
    to.save()
    return JsonResponse([],safe=False)


def ajaxCancelTO(request):

    idTO = request.GET.get('idTransferOrder')
    to = TransferOrder.objects.get(pk=int(idTO))
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idProduct
        aw.unitsReserved = aw.unitsReserved - int(wew[x].qty)
        print(aw.unitsInStock)
        aw.unitsInStock = aw.unitsInStock + int(wew[x].qty)
        print(aw.unitsInStock)
        aw.save()
    to.status = "Cancelled"
    to.save()
    return JsonResponse([],safe=False)