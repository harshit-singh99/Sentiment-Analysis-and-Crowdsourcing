from django.test import TestCase
from .models import Movie, Rests
# Create your tests here.


class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title='newmovie1', director='newdirector1')

    def test_get_fields(self):
        newmovie1 = Movie.objects.get(title='newmovie1')
        self.assertEqual(newmovie1.get_fields(), [('Title', 'newmovie1'), ('Director', 'newdirector1')])


class RestsTestCase(TestCase):
    def setUp(self):
        Rests.objects.create(title='restaurant1', cuisine='cuisine1', location='location1')

    def test_get_fields(self):
        newrest = Rests.objects.get(title='restaurant1')
        self.assertEqual(newrest.get_fields(),
                         [('Name', 'restaurant1'), ('Cuisine', 'cuisine1'), ('Location', 'location1')])
