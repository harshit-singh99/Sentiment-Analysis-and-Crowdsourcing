from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieSerializer, RestsSerializer, ReviewSerializer
from one_page.models import Movie, Rests, Unlabeled
from predictReview.utils import cleantext, mov, restr

class MovieView(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        id = request.data
        try:
            rest = Movie.objects.get(pk=id)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(pk=id)
        reviews = movie.unlabeled.all().order_by('-pk')[:5]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class RestsView(APIView):

    def get(self, request):
        rests = Rests.objects.all()
        serializer = RestsSerializer(rests, many=True)
        return Response(serializer.data)

    def post(self, request):
        id = request.data
        try:
            rest = Rests.objects.get(pk=id)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        reviews = rest.unlabeled.all().order_by('-pk')[:5]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class Predict(APIView):

    def get(self, request):
        return Response({"type": "movie/restaurant", "review": "review"})

    def post(self, request):
        data = request.data
        typeof = data['type']
        review = data['review']
        clean = cleantext(review)
        if typeof == 'movie':
            prediction = mov.predict([clean])
        elif typeof == 'restaurant':
            prediction = restr.predict([clean])
        else:
            return Response({"error": "not a valid type"}, status=status.HTTP_400_BAD_REQUEST)
        prediction = 'Positive' if prediction[0] == 'p' else 'Negative'
        return Response({'prediction': prediction})
