from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .data_analysis import get_stats
from one_page.models import *
import pandas as pd
from credits.models import AccountBalance,Statement
from django.http import HttpResponse
import uuid

# Create your views here.
options = {'movie': Movie, 'restaurant': Rests}#small,singular
@login_required(login_url='login')
def main_view(request):
    context = {'options': options.keys()}
    return render(request, 'dataAnalysis/main_page.html', context=context)


def show_list(request):
    if request.method == 'POST':
        option = options[request.POST['option']]
        context = {'list': option.objects.all()}
        return render(request, 'dataAnalysis/list.html', context=context)
    else:
        return redirect('data_analysis')


def stats(request):
    if request.method == 'POST':
        temp = AccountBalance.objects.get(user=request.user)
        if float(temp.balance) > 200:
            option = request.POST['option']
            option1 = options[option]
            idd = int(request.POST['idd'])
            idd1 = option1.objects.get(pk=idd)
            unlabeled_count = len(idd1.unlabeled.all())#send to django
            name = idd1.get_fields()[0][1]

            lst = option1.objects.all()#list of movies
            names = []
            genders = []
            reviews = []
            polarities = []
            locations = []
            #code to get the data frame
            '''
            dta = [(i.title,j.review,j.polarity,usertable[j.userid].gender) for j in i.labeled.all() for i in lst]
            complete = pd.DataFrame(dta, columns=[option,'text','polarity','gender'])
            '''
            for i in lst:
                rev_objs = i.labeled.all()
                fields = dict(i.get_fields())
                for j in rev_objs:
                    reviews.append(j.review)
                    names.append(i.title)
                    if j.polarity:
                        polarities.append('p')
                    else:
                        polarities.append('n')
                    genders.append(j.user.userprofile.gender)
                    if 'Location' in fields:
                        locations.append(i.location)

            dct = {option:names,'text':reviews,'polarity':polarities,'gender':genders}
            if len(locations):
                dct['location'] = locations
            complete = pd.DataFrame(dct)

            total_stats,pos_stats,neg_stats = get_stats(complete,name,option)#send to django
            posper = pos_stats['count']/total_stats['count']*100
            negper = neg_stats['count']/total_stats['count']*100
            context = {'new_count':unlabeled_count,'posper':posper,'negper':negper,
            'total_stats':total_stats,'pos_stats':pos_stats,'neg_stats':neg_stats,
            'type':option,'name':name}
            AccountBalance.objects.filter(user=request.user).update(balance=temp.balance-200)
            Statement.objects.create(user=request.user,transaction_id="PSA"+uuid.uuid4().hex[:9].upper(),amount=200)
            return render(request, 'dataAnalysis/graphs.html', context)
        else:
            return HttpResponse('<html><head><script>alert("You dont have sufficient funds");window.location="/data_analysis";</script></head></html>')
    else:
        #return HttpResponse(status = 400)
        return redirect('data_analysis')