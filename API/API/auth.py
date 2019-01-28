from django.contrib import auth
from django.contrib.auth.models import User

def validate(username, password):
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        return False
    if not user.password == password:
        return False
    return True
