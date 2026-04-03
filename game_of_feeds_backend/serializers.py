from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        default_url = 'https://res.cloudinary.com/dctqmaht5/image/upload/v1752109202/default_profile_idzhze.jpg'
        stored = str(obj.profile.profile_image) if obj.profile.profile_image else ''
        if not stored or stored == 'game_of_feeds/default_profile_idzhze':
            return default_url
        url = obj.profile.profile_image.url
        return url.replace('http://', 'https://', 1)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )