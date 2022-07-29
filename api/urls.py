from django.urls import path
from . import views
urlpatterns = [
    path('posts/', views.posts, name='posts'),
    #path('posts/<str:post_id>/', views.posts, name='post'),
    # path('login/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', TokenVerifyView.as_view(), name='token_verify'),
]
