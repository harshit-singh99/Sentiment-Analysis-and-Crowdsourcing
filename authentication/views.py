from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import CustomUserCreationForm,LoginForm,UserupdateForm,ProfileupdateForm,Createprofileform
from one_page.models import Unlabeled
from django.contrib.auth.models import User
from credits.models import AccountBalance
from .models import Userprofile
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from credits.models import AccountBalance

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

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request,user,backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('profile_new')
#     else:
#         form = CustomUserCreationForm()
#         form2 = Createprofileform()
#
#     return render(request, 'authentication/reg_new.html',{'form': form})
#
# def profile_form(request):
#     if request.method == 'POST':
#         form2 = Createprofileform(request.POST, request.FILES)
#         if form2.is_valid():
#             user = request.user
#             print(user)
#             profile = form2.save()
#             profile.user = user
#             profile.save()
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('home')
#     else:
#         form2 = Createprofileform()
#
#     return render(request, 'authentication/profile_new.html', {'form2': form2})
#

def register(request):
    if request.method == 'POST':
        u_form = CustomUserCreationForm(data=request.POST)
        p_form = Createprofileform(data=request.POST)
        print("forms are not valid")

        if u_form.is_valid() and p_form.is_valid():
            print('forms are valid')
            user = u_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            print('helloooo','password set')
            user.save()

            profile = p_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            AccountBalance.objects.create(user=user, balance=100)

            current_site = get_current_site(request)
            mail_subject = 'Activate your  account.'
            message = render_to_string('authentication/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = u_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            # profile = p_form.save(commit=False)
            # profile.user = user
            #
            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']
            #
            # profile.save()

            #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # AccountBalance.objects.create(user=user, balance=100)
            #return redirect('home')
    else:
        u_form = CustomUserCreationForm()
        p_form = Createprofileform()

    return render(request, 'authentication/new.html', {'u_form': u_form,'p_form':p_form})





def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def profile_view(request):

    try:

        review = []
        review.append(Unlabeled.objects.filter(user = request.user)[0].review)

        return render(request, "authentication/profile.html",{'user':request.user, 'Unlabeled':Unlabeled, 'review':review})
    except:
        return render(request, "authentication/profile.html",
                      {'user': request.user, 'Unlabeled': Unlabeled})




def edit_profile(request):
    if request.method == 'POST':
        userupdateform = UserupdateForm(request.POST,instance=request.user)
        profileupdateform = ProfileupdateForm(request.POST,
                                              request.FILES,
                                              instance=request.user.userprofile)
        if userupdateform.is_valid() and profileupdateform.is_valid():
            userupdateform.save()
            profileupdateform.save()
            return redirect('profile')
    else:
        user1 = User.objects.filter(username = request.user.username).first()
        if Userprofile.objects.filter(user = user1):

            userupdateform = UserupdateForm(instance=request.user)
            profileupdateform = ProfileupdateForm(instance=request.user.userprofile)
        else:
            Userprofile.objects.create(user = user1)
            userupdateform = UserupdateForm(instance=request.user)
            profileupdateform = ProfileupdateForm(instance=request.user.userprofile)

        if AccountBalance.objects.filter(user=user1):
           pass
        else:
            AccountBalance.objects.create(user=user1,balance=100)

    return render(request,'authentication/editprofile.html',{'uform':userupdateform , 'pform':profileupdateform})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return render(request,'authentication/after_active.html')
    else:
        return HttpResponse('Activation link is invalid!')
