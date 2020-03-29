from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie.models import MovieInfo, ShowDetail, MovieGenre

from datetime import datetime

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = ["genre","movie"]
        read_only_fields = ["movie"]

class AddMovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    genre = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    class Meta:
        model = MovieInfo
        fields = ["name","description","run_time","buffer","genre","id"]

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        movie_object = super().create(validated_data)
        for val in genres:
            MovieGenre.objects.get_or_create(movie_id=movie_object.id, genre=val)

        return movie_object

class AddMovieShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    booked_seats = serializers.IntegerField(read_only=True)
    class Meta:
        model = ShowDetail
        fields = ["movie","showdate","total_seats","id","booked_seats"]

    def create(self, validated_data):

        showdatetimestamp = validated_data.get('showdate').timestamp()
        queryset = list(ShowDetail.objects.filter(movie_id=validated_data.get('movie').id).values_list('showdate',flat=True))
        movie_obj = MovieInfo.objects.get(id=validated_data.get('movie').id)
        buffer_string = movie_obj.buffer.isoformat()
        duration_string = movie_obj.run_time.isoformat()
        buffer_point = datetime.strptime(buffer_string,'%H:%M:%S')
        duration_point = datetime.strptime(duration_string,'%H:%M:%S')
        total_seconds = buffer_point.second + duration_point.second + (buffer_point.minute+duration_point.minute)*60 + (buffer_point.hour+duration_point.hour)*3600
        
        for date in queryset:
            print(abs(showdatetimestamp-date.timestamp()))
            if(abs(showdatetimestamp-date.timestamp())<total_seconds):
                raise ValidationError("Already Exist")
            else:
                continue

        
        show_object = super().create(validated_data)

        return show_object
