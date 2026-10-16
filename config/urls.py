from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterView, StaffTokenObtainPairView, UserProfileView


urlpatterns = [
    path("api/auth/register", RegisterView.as_view(), name="register"),
    path("api/auth/me", UserProfileView.as_view(), name="user-profile"),
    path(
        "api/auth/login",
        StaffTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("properties.urls")),
    path("api/", include("members.urls")),
    path("api/", include("contracts.urls")),
]
