from django.contrib import admin
from .models import Movie, Rests, Unlabeled, Labeled

admin.site.register(Movie)
admin.site.register(Rests)
admin.site.register(Unlabeled)
admin.site.register(Labeled)
# Register your models here.
