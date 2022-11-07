from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomObtainTokenPairView, UserRegisterView

urlpatterns = [
    path("auth/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
]
