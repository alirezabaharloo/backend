from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from mail_templated import send_mail


def send_resset_password_mail(email='alireza.baharlou.0862@gmail.com', token=None):
    pass
    # template_path = 'email.tpl'
    # context = {
    #     'token': token,
    #     'email': email
    # }
    # from_email = settings.EMAIL_HOST_USER

    # send_mail(template_path, context, from_email, [email])



def permission_detector(**kwargs):
    user_permissions = []
    for perm, perm_bool  in kwargs.items():
        if perm_bool:
            user_permissions.append(perm)

    return ','.join([perm for perm in user_permissions]) if user_permissions else 'normal'

