from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

options = {'Movies': Movie, 'Restaurants': Rests}
# fields = {'Movies': Movie._meta.get_fields(), 'Restaurants': Rests._meta.get_fields()}


@login_required(login_url='login')
def main_view(request):
    context = {'options': options.keys()}
    return render(request, 'one_page/main_page.html', context=context)


def show_list(request):
    option = options[request.POST['option']]
    context = {'list': option.objects.all()}
    return render(request, 'one_page/list.html', context=context)


def show_reviews(request):
    option = request.POST['option']
    option1 = options[option]
    idd = int(request.POST['idd'])
    idd1 = option1.objects.get(pk=idd)

    reviews = idd1.unlabeled.all().order_by('-pk')[:5]
    context = {'reviews': reviews, 'option': option, 'idd': idd, 'details': idd1.get_fields()}
    return render(request, 'one_page/reviews.html', context=context)


def write_review(request):
    option = options[request.POST['option']]
    idd = int(request.POST['idd'])
    new_data = request.POST['review']
    user1 = request.user
    content_object = option.objects.get(pk=idd)
    Unlabeled.objects.create(content_object=content_object, review=new_data,user=user1)
    return HttpResponse(status=200)