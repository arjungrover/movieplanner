from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from movie.serializers import AddMovieSerializer, AddMovieShowSerializer, GenreSerializer
from movie.models import MovieInfo, ShowDetail, MovieGenre


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = AddMovieSerializer
    queryset = MovieInfo.objects.all()
    
   
class MovieShowViewSet(viewsets.ModelViewSet):
    serializer_class = AddMovieShowSerializer
    queryset = ShowDetail.objects.all()


class GetAllMovies(ListAPIView):
    
    def get(self, request, *args, **kwargs):
        queryset = MovieInfo.objects.all()
        serializer = AddMovieSerializer(queryset, many=True)
        
        return Response(serializer.data)


class GetAllShows(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        queryset = ShowDetail.objects.filter(movie__id=request.GET.get('id'))
        serializer = AddMovieShowSerializer(queryset, many=True)

        return Response(serializer.data)
