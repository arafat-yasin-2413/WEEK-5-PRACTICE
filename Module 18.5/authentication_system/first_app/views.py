from django.shortcuts import render,redirect
from first_app.forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home.html')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Account Created Successfully')
                form.save()
        else:
            form = SignUpForm()
        return render(request,'signup.html',{'form':form})
    else:
        return redirect('profile')




def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('signup')




def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                messages.success(request,'Logged In Successfully')
                name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                user = authenticate(username=name,password = user_pass)
                if user is not None:
                    login(request,user)
                    return redirect('profile')
        else:
            form = AuthenticationForm()
        return render(request,'login.html',{'form':form})
    else:
        return redirect('profile')



def user_logout(request):
    
    messages.success(request,'Logged Out Successfully')
    logout(request)
    return redirect('homepage')
    

def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                
                update_session_auth_hash(request,form.user)
                messages.success(request,'Password Changed Successfully')
                return redirect('profile')
        else:
            form = PasswordChangeForm(user = request.user)
        return render(request,'password_change.html',{'form':form,'user':request.user})
    else:
        return redirect('login')
    

def password_change2(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = SetPasswordForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                messages.success(request,'Password Change Without Old PWD Successfull')
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'password_change.html',{'form':form})
    else:
        return redirect('login')