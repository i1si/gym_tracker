from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import main.views as v


urlpatterns = [
    path('', v.index, name='main'),
]
