from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from one_page.models import Unlabeled, Labeled
from .models import Question
from credits.models import AccountBalance,Statement
import uuid

@login_required(login_url='login')
def crd_scr_get(request):
    labs = Labeled.objects.all().order_by('?')[0:3]
    unlab = Unlabeled.objects.all().order_by('?')[0]
    try:
        a = Question.objects.get(user=request.user)
        a.delete()
    except:
        pass

    Question.objects.create(qid1=labs[0], qid2=labs[1], qid3=labs[2], qid4=unlab, user=request.user)
    questions = Question.objects.get(user=request.user)
    review1 = questions.qid1.review
    review2 = questions.qid4.review
    review3 = questions.qid2.review
    review4 = questions.qid3.review

    print(Question.objects.get(user=request.user))
    # questions.save()
    context = {'review1': review1, 'review2': review2, 'review3': review3, 'review4': review4}
    return render(request, 'crowdSourcing/crdscr_main.html', context)



@login_required(login_url='login')
def crd_scr_post(request):
    print(request.POST)
    ans1 = request.POST['ans1']
    ans2 = request.POST['ans2']
    ans3 = request.POST['ans3']
    ans4 = request.POST['ans4']

    asked_ques = Question.objects.get(user=request.user)
    if int(ans1) == int(asked_ques.qid1.polarity) and int(ans3) == int(asked_ques.qid2.polarity) and int(
            ans4) == int(asked_ques.qid3.polarity):
        temp = AccountBalance.objects.get(user=request.user)
        bal = float(temp.balance)+float(1)
        AccountBalance.objects.filter(user=request.user).update(balance=bal)
        Statement.objects.create(user=request.user,amount=1,transaction_id="CS"+uuid.uuid4().hex[:9].upper())
        unlab = asked_ques.qid4
        if int(ans2) == 1:
            unlab.score = unlab.score + 1
            asked_ques.qid4.save()
            if unlab.score >= 10:
                #Labeled.objects.create(review=unlab.review, polarity=True, content_object=unlab.content_object)
                Labeled.objects.create(review=unlab.review, user=unlab.user, polarity=True, time=unlab.time, content_object=unlab.content_object)
                unlab.delete()
        elif int(ans2) == 0:
            unlab.score = unlab.score - 1
            asked_ques.qid4.save()
            if unlab.score <= -10:
                #Labeled.objects.create(review=unlab.review, polarity=False, content_object=unlab.content_object)
                Labeled.objects.create(review=unlab.review, user=unlab.user, polarity=False, time=unlab.time, content_object=unlab.content_object)
                unlab.delete()
    try:
        asked_ques.delete()
    except:
        pass

    return redirect('crdscr_main')
