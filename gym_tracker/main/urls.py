from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import main.views as v


urlpatterns = [
    path('', v.index_view, name='main'),
    path('users/register/', v.register_view, name='register'),    
    path('users/logout/', v.logout_view, name='logout'),
    path('users/login/', v.login_view, name='login'),
    path('progress/', v.progress_view, name='progress'),
    path('trainings/', v.trainings_view, name='trainings'),
    path('trainings/<int:training_id>', v.training_view, name='training'),
    path('running/', v.running_view, name='running'),
]
