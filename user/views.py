import random
import string
import time

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction

from .models import User


class Authentication(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["POST"], detail=False, url_path="auth")
    def authorization_user_with_phone(self, request):
        try:
            phone_number = request.data.get('phone_number')
            if phone_number is not None and 10 <= len(phone_number) <= 12:
                random_code = random.randrange(1000, 10000)
                request.session['random_code'] = random_code
                request.session['phone_number'] = phone_number
                time.sleep(2)
                return Response({'detail': f'Код подтверждения: {random_code}'})
            else:
                return Response({'error': 'С Вашим номером какая-то проблема. Попробуйте еще раз'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'С Вашим номером какая-то проблема. Попробуйте еще раз'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, url_path="accept_user")
    def authorization_user_with_code(self, request):
        try:
            phone_number = request.session.get("phone_number")
            try:
                code = int(request.data.get('code'))
            except TypeError:
                code = None
            try:
                random_code = int(request.session.get('random_code'))
            except TypeError:
                random_code = None
            if code == random_code:
                try:
                    user = User.objects.get(
                        phone_number=phone_number)
                except ObjectDoesNotExist:
                    user = User.objects.create(
                        phone_number=phone_number,
                        invite_code=None,
                        invite_code_for_users=''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    )
                refresh = RefreshToken.for_user(user)
                serializer = self.serializer_class(user, many=False)
                return Response([serializer.data, {'access': str(refresh.access_token)}])
            else:
                return Response({'error': 'Вы ввели неверный код. Попробуйте еще раз'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'В Ваших данных присутствует ошибка. Попробуйте еще раз'},
                            status=status.HTTP_400_BAD_REQUEST)


class Profile(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["GET"], detail=False)
    def info(self, request):
        return Response(self.get_serializer(request.user, many=False).data)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def change_profile(self, request):
        user = request.user
        invite_code = request.data.get("invite_code")
        try:
            inviting_user = User.objects.get(invite_code_for_users=invite_code)
        except ObjectDoesNotExist:
            return Response({"detail": "Похожу Вы ввели неверный код, повторите попытку"}, 200)

        if user.invite_code is None:
            user.invite_code = invite_code
            user.save()
            return Response({"detail": "Реферальный код подтвержден"}, 200)
        else:
            return Response({'detail': "Ваш реферальный код уже был использован ранее."}, 200)
