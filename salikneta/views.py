from django.shortcuts import render,redirect

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
