from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import Authentication
from .views import Profile

router = DefaultRouter()

router.register('auth', Authentication)
router.register('profile', Profile)
urlpatterns = router.urls

urlpatterns += [
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]

