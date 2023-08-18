from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'invite_code_for_users', 'invited_users',)

    def get_invited_users(self, obj):
        return User.objects.filter(invite_code=obj.invite_code_for_users).values_list('phone_number', flat=False)
