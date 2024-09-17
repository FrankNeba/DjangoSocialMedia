from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import random

def mail(message, subject, recipient):
    send_mail(
        subject = subject,
        message= message,
        recipient_list= [recipient],
        from_email='',
        fail_silently=False

    )

def home(request):
    return render(request, 'authenticate/index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'An account exists with email {email}')
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'An account exists with username {username}')

        elif password != passwordConfirm:
            messages.error(request, 'Passwords don\'t match')

        elif len(password) < 8:
            messages.error(request, 'Password too short')

        # elif True:
            # messages.error(request, 'Password can easily be guessed')

        else: 
            code = random.randint(11111, 99999)
            user = User(username=username, email=email, password = make_password(password))
            user.code = code
            user.is_active = False
            user.save()
            login(request, user)
            message = f'Hello {username},\nYour Socia account verification code is {code}'
            subject = f'Account Verifcation'
            mail(message=message, subject=subject, recipient=user.email)
            return redirect('account_verification', pk=user.id)
        
    return render(request, 'authenticate/signup.html')

# @login_required(login_url='login')
def accountActivation(request, pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            user.is_active = True
            user.save()
            messages.success(request, 'Account verified, login to continue')
            return redirect('login')
        messages.error(request, 'Invalid code')
    return render(request, 'authenticate/accountActivation.html')


@login_required(login_url='login')
def logUserOut(request):
    logout(request)
    return redirect('home')


def logUserIn(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password= password)

        #if user exists and authentication is correct
        if user is not None:
            login(request, user)
            return redirect('home')
                
        try:
            user = User.objects.get(email = email)
            if user.check_password(password):
                code = random.randint(111111, 999999)
                user.code = code
                user.save()
                message = f'Hello {user.username},\nYour Socia account is not activated.\nYour Socia account verification code is {code}'
                subject = f'Account Verifcation'
                mail(message=message, subject=subject, recipient=user.email)
                messages.success(request,'Account not vierified. ')
                return redirect('account_verification', pk=user.id)
        
        except:
            messages.error(request,'incorrect email or password')
    
    return render(request,'authenticate/login.html') 

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            code = random.randint(111111, 999999)
            user.code = code
            user.save()
            message = f'Hello {user.username},\nYour Socia account password reset code is {code}'
            subject = f'Reset password'
            mail(message=message, subject=subject, recipient=user.email)
            return redirect('password_reset_code', pk=user.id)
        except:
            messages.error(request,f'No user with email {email}')
    
    return render(request, 'authenticate/forgotPassword.html')

def resetPasswordCode(request,pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            return redirect('reset_password', pk=user.id)
        messages.error(request, 'Invalid code')
    return render(request, 'authenticate/accountActivation.html')

def resetPassword(request, pk):
    if request.method == 'POST':
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']

     
        if password != passwordConfirm:
            messages.error(request, 'Passwords don\'t match')

        elif len(password) < 8:
            messages.error(request, 'Password too short')

        elif str.isdigit(password):
            messages.error(request,'Password can easily be guessed. Use a combination of numbers, letters and symbols')

        else:
            user = User.objects.get(id = pk)
            user.password = make_password(password)
            user.save()
            return redirect('login')
    return render(request, 'authenticate/resetPassword.html') 

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name= request.POST['lastname']
        if request.FILES.get('image') is not None:
            user.image = request.FILES['image']
        user.save()
        messages.success(request,'Profile Updated succesfully')
    return render(request, 'authenticate/updateProfile.html', {'user':user})



        






# Create your views here.
