from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="homepage"),
    path('workout', views.workout, name="workouts")
    # path('room/<str:pk>/', views.room, name="room")
]