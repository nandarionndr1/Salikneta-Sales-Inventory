from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'salikneta/login.html')
def log_in(request):
    return render(request, 'salikneta/login.html')
def verify(request):
    user = None
    try:
        #fix logging dogging.
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
    except:
        None
    if request.method == 'POST':
        if user is not None:
            request.session['username'] = user.username
            request.session['guest'] = True
            request.session['logged'] = True
            login(request, user)
        else:
            messages.warning(request, 'Wrong credentials, please try again.')
        return redirect('home')
    else:
        return redirect('index')
def home(request):
    return render(request, 'salikneta/home.html')
def signout(request):
    return redirect('index')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        usertype = request.POST.get('usertype')
        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)

        if usertype == "os":
            group = Group.objects.get(name="Operations Supervisor")
            user.groups.add(group)
        elif usertype == "gk":
            group = Group.objects.get(name="Gamekeeper")
            user.groups.add(group)
        elif usertype == "own":
            group = Group.objects.get(name="Owner")
            user.groups.add(group)

        user.save()
        messages.warning(request, 'Account Created.')
        return redirect('index')
    return render(request, 'octo_site/user_module/register.html', {'branches':Branch.objects.all()})
