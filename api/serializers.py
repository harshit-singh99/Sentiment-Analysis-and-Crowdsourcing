from one_page.models import Movie, Rests, Unlabeled
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'id')


class RestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rests
        fields = ('title', 'id')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unlabeled
        fields = ('review', 'time')
