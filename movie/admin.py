from django.contrib import admin
from movie.models import MovieGenre, ShowDetail, MovieInfo, UserMovie

admin.site.register(MovieGenre)
admin.site.register(ShowDetail)
admin.site.register(MovieInfo)
admin.site.register(UserMovie)
