from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 

def home(request):
    users =User.objects.filter(is_superuser=True)
    print(users)
    return render(request,'index.html')
# Create your views here.
def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('register')
            else: 
                user = User.objects.create_user(username=username,  password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                messages.success(request,'User Created successfully')
                return redirect('login')
        else:
            messages.info(request,'password not match')
            return redirect('register')
    else:
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.info(request,'login successful.')
            return redirect('home')
        else:
            messages.info(request,'invalid credentials.')
            return redirect('login')
        
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'logout successful.')
    return redirect('home')

