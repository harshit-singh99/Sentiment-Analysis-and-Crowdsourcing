from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import CustomUserCreationForm,LoginForm



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.login(request)

            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:

                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'authentication/login_new.html',{'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/reg_new.html',{'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


