from rest_framework import serializers
from followers.models import Follower
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(required=False)
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request and request.user.is_authenticated else False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        stored = str(instance.profile_image) if instance.profile_image else ''
        default_url = 'https://res.cloudinary.com/dctqmaht5/image/upload/v1752109202/default_profile_idzhze.jpg'
        if not stored or stored == 'game_of_feeds/default_profile_idzhze':
            data['profile_image'] = default_url
        else:
            url = instance.profile_image.url
            data['profile_image'] = url.replace('http://', 'https://', 1)
        return data

    def get_following_id(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            following = Follower.objects.filter(owner=user, followed=obj.owner).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'username',
            'display_name',
            'bio',
            'house',
            'profile_image',
            'created_at',
            'updated_at',
            'is_owner',
            'following_id',
            'posts_count',
            'followers_count',
            'following_count',
        ]