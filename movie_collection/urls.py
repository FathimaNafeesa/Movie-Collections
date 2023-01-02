from django.urls import path

from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/<int:user_id>/', views.ListMovieView.as_view(), name='detail'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('collections/<int:user_id>/', views.CreateCollectionsView.as_view(), name='collections'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('request-count/', views.RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', views.RequestCountView.as_view(), name='request-count'),
    path('create_task/', views.CreateTaskView.as_view(), name='create_task'),
    path("task/", views.task_view, name="task_view"),
]
