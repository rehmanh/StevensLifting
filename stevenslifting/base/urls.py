from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="homepage"),
    path('workouts', views.workouts, name="workouts"),
    path('workout/<str:pk>', views.workout, name="workout"),
    path('workout/set/<str:pk>/update', views.update_set, name="updateSet")
]