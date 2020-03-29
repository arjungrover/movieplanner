from django.db import models
from base.models import BaseModel
from user.models import UserInfo
from collections import namedtuple
from datetime import datetime

class MovieInfo(BaseModel, models.Model):
    """
    This model will store details about movies
    """

    name = models.CharField(verbose_name="Movie Name",max_length=128, unique=True)
    description = models.TextField(verbose_name="Movie Description")
    run_time = models.TimeField(verbose_name="Movie Duration")
    buffer = models.TimeField(verbose_name="Buffer Time")
   
    def __str__(self):
        return "{} : {}".format(self.name, self.run_time)

class  MovieGenre(BaseModel, models.Model):
    """
    This model will be give information about genres of movies
    """
    
    TYPE = namedtuple('TYPE', ['ACTION','ADVENTURE','COMEDY','CRIME','DRAMA','HISTORICAL'])(
        ACTION=1,
        ADVENTURE=2,
        COMEDY=3,
        CRIME=4,
        DRAMA=5,
        HISTORICAL=6
    )
    GENRE_TYPE = [
        (TYPE.ACTION, 'Action'),
        (TYPE.ADVENTURE, 'Adventure'),
        (TYPE.COMEDY, 'Comedy'),
        (TYPE.CRIME, 'Crime'),
        (TYPE.DRAMA, 'Drama'),
        (TYPE.HISTORICAL, 'Historical')

    ]
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE, null=False)
    genre = models.IntegerField(verbose_name='Genre', choices=GENRE_TYPE)
    
    def __str__(self):
        return "{} ".format(self.genre)

class ShowDetail(BaseModel, models.Model):
    """
    This model will be used to give details about particular movie show
    """
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE, null=False)
    showdate = models.DateTimeField(default=datetime.now())
    total_seats = models.PositiveIntegerField(verbose_name="Total Seats", default=0)
    booked_seats = models.PositiveIntegerField(verbose_name="Booked Seats", default=0)
    
    def __str__(self):
        return "{} : {}".format(self.movie, self.total_seats)


class UserMovie(BaseModel, models.Model):
    """
    This model will store details about user selected show
    """

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=False)
    show = models.ForeignKey(ShowDetail, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.user)
