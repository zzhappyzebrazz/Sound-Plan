from player.models import Artist, Album, Song
from rest_framework import serializers, status
from rest_framework.response import Response

class SongSerializers(serializers.HyperlinkedModelSerializer):
    album = serializers.IntegerField(source='album_id')
    artists = serializers.IntegerField(source='artists_id')

    class Meta:
        model = Song
        fields = "__all__"

    def create(self, validated_data):
        return Song.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.song_name = validated_data.get('song_name', instance.song_name)
        instance.audio = validated_data.get('audio', instance.audio)
        instance.artists = validated_data.get('artists', instance.artists)
        return instance

    def destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AlbumSerializers(serializers.HyperlinkedModelSerializer):
    artists = serializers.IntegerField(source='artists_id')

    class Meta:
        model = Album
        fields = "__all__"

    def create(self, validated_data):
        return Album.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.artists = validated_data.get('artists', instance.artists)
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.album_cover = validated_data.get('album_cover', instance.album_cover)
        instance.public_day = validated_data.get('public_day', instance.public_day)
        return instance

    def destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ArtistSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Artist
        fields = "__all__"

    def create(self, validated_data):
        return Song.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.artist_name = validated_data.get('artist_name', instance.artist_name)
        instance.avartar = validated_data.get('avartar', instance.avartar)
        return instance

    def destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)