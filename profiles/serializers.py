from rest_framework import serializers
from followers.models import Follower
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    profile_image = serializers.ReadOnlyField(source='image.url')

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request and request.user.is_authenticated else False

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
        ]