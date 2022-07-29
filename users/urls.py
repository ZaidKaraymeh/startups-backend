from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.users, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('login/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', TokenVerifyView.as_view(), name='token_verify'),
]