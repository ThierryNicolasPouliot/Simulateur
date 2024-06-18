# simulation/decorators.py
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(
        lambda user: user.is_superuser, login_url='/admin/login/'
    )(view_func)
