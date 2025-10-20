from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)