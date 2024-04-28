from django.contrib.auth.forms import UserCreationForm

from main.models import CustomUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
