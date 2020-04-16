from django.conf.urls import url
from django.views.generic import TemplateView
from .views import Index, Profile, Register, Activation, ActivationResend

from django.contrib.auth.decorators import login_required

""" URL's para llevar a cabo el registro y la activacion

1. Registro -> template 'registration_form.html'

    1.1 Registro completo -> template 'registration_complete.html'

2. Activacion -> template 'activate.html'

    2.1 Creacion de email

        2.1.1 Cuerpo del mensaje -> Archivo 'activation_email.txt' y 'activation_email.html'

        2.1.2 Asunto del mensaje -> Archivo 'activation_email_subject.txt'

    2.2 Activacion completa -> template 'activation_complete.html'

Cantidad de URL's es equivalente a la cantidad de plantillas (templates) = 4

"""
app_name="user"
urlpatterns = [
    url(r'^$', Index.as_view(), name="index"),
    url(r'^register/$', Register.as_view(), name='registration_register'),
    url(r'^register/complete$', TemplateView.as_view(template_name = 'registration/registration_complete.html'), name='registration_complete'),
    url(r'^activate/resend/$',  ActivationResend.as_view(), name='registration_resend_activation'),
    url(r'^activation/(?P<activation_key>\w+)/$', Activation.as_view(),  name='registration_activate'),
    url(r'^activation/complete$', TemplateView.as_view(template_name='registration/activation_complete.html'),  name='registration_activation_complete'),
    url(r'^profile/', login_required(Profile.as_view()), name="profile")
]