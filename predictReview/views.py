from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import *
from credits.models import AccountBalance, Statement
import uuid


@login_required(login_url='login')
def predict_review(request):
    result = ''
    review_ph = "Enter your review here"
    if request.method == 'POST':
        review_type = request.POST['search_categories']
        print(review_type)
        review = request.POST['review']
        review_ph = review
        clean = cleantext(review)

        if review_type == 'movie':
            pred = mov.predict([clean])
        elif review_type == 'restaurant':
            pred = restr.predict([clean])

        if pred[0] == 'p':
            result = 'positive'
        elif pred[0] == 'n':
            result = 'negative'
    context = {'review_ph': review_ph, 'result': result}
    return render(request, 'predictReview/predict.html', context)


@login_required(login_url='login')
def batch_predict(request):
    result = ''
    if request.method == 'POST':
        temp = AccountBalance.objects.get(user=request.user)
        bal = float(temp.balance) - float(200)
        if bal >= 0:
            file1 = request.FILES.get('fileupload')
            review_type = request.POST.get('type')
            if file1 == None:
                result = 'No file uploaded.'
                return render(request, 'predictReview/batch_predict.html', {'result': result})

            ext = file1.name
            if ((not ".txt" in ext) or (file1.content_type != 'text/plain')) and (
                    (not ".csv" in ext) or (file1.content_type != 'application/vnd.ms-excel')):
                result = 'Please upload .txt file only.'
                return render(request, 'predictReview/batch_predict.html', {'result': result})

            lst = file1.read().splitlines()
            nlist = []
            for i in lst:
                nlist.append(i.decode('utf-8'))

            clean = map(cleantext, nlist)
            if review_type == 'movie':
                pred = mov.predict(clean)
            elif review_type == 'restaurant':
                pred = restr.predict(clean)
            pos_count = 0
            neg_count = 0
            pos_per = 0
            for i in pred:
                if i == 'p':
                    pos_count += 1  # send to django
                elif i == 'n':
                    neg_count += 1  # send to django
            total_count = pos_count + neg_count  # send to django
            pos_per = pos_count / total_count * 100  # send to django
            result = "Positive review: " + str(pos_count) + "\nNegative review: " + str(
                neg_count) + "\nPercentage of positive review: " + str(pos_per) + "%"
            # temp = AccountBalance.objects.get(user = request.user)
            # bal = float(temp.balance)-float(50)
            AccountBalance.objects.filter(user=request.user).update(balance=bal)
            Statement.objects.create(user=request.user, amount=200, transaction_id="PSA" + uuid.uuid4().hex[:9].upper())
            # return render(request, 'predictReview/batch_predict.html', {'result' : result})
        else:
            result = "Insufficient Credits "

    return render(request, 'predictReview/batch_predict.html', {'result': result})
