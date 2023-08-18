from django.contrib.auth.backends import ModelBackend
from user.models import User


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None