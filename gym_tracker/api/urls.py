from django.urls import path, include
from rest_framework import routers

import api.views as v


router = routers.DefaultRouter()
router.register(r'users', v.UserInfoViewSet, basename='user')
router.register(r'trainings', v.TrainingViewSet, basename='last_training')
router.register(r'exercises', v.FinishedExerciseViewSet, basename='exercises')

urlpatterns = [
    path('', include(router.urls)),
    path('users/login', v.login_view)
]
