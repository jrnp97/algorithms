from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

#Modulos necesarios tanto para registro y activacion
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

#Modulos necesarios para configuracion primordial de registro
from registration.models import RegistrationProfile
from registration import signals
from .forms import UserRegisterForm
from registration.views import RegistrationView


#Importando la vistas para configuracion de activacion
from registration.backends.default.views import ActivationView, ResendActivationView

#Modulo para el tiempo
from datetime import datetime

#Importando recursos de Tweet
from Twitts.models import Twitts
from Twitts.forms import TwittForm
from Twitts.views import Tview

# Create your views here.

#Creando la vista para el manejo de la activacion
class Activation(ActivationView):
    registration_profile = RegistrationProfile

    def activate(self, *args, **kwargs):
        activation_key = kwargs.get('activation_key', '')
        site = get_current_site(self.request)
        print (site)
        activated_user = (self.registration_profile.objects
                          .activate_user(activation_key, site))
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=self.request)
        return activated_user

    def get_success_url(self, user):
        return ('user:registration_activation_complete', (), {})

class ActivationResend(ResendActivationView):
    registration_profile = RegistrationProfile

    def resend_activation(self, form):
        site = get_current_site(self.request)
        email = form.cleaned_data['email']
        return self.registration_profile.objects.resend_activation_mail(
            email, site, self.request)

    def render_form_submitted_template(self, form):
        email = form.cleaned_data['email']
        context = {'email': email}
        return render(self.request,
                      'registration/resend_activation_complete.html',
                      context)
#Creando la vista para registro
class Register(RegistrationView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:registration_complete')#activation view

    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
    registration_profile = RegistrationProfile

#Configurando el registro del usuario fuente:https://github.com/macropin/django-registration/blob/master/registration/backends/default/views.py

    def register(self, form):
        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (User.objects
                                 .create_user(**form.cleaned_data))

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

class Index(ListView):
    model = Twitts
    template_name = 'index.html'
    #Declarando cantidad de objetos por "pagina"
    paginate_by = 3


class Profile(CreateView):
    model = Twitts
    template_name = 'user/profile.html'
    form_class = TwittForm
    success_url = reverse_lazy('user:profile')

    #Sobreescribiendo el metodo get para mostrar twitts del usuario
    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)

        if 'twitts' not in context:
            context['twitts'] = Tview(User.objects.get(id=User.objects.filter(username=self.request.user)))
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
            #User.objects.get(id=User.objects.filter(username=self.request.user)).id
        return context


    #Sobreescribiendo el metodo post para guardar el twitt correctamente
    def post(self, request, *args, **kwargs):
        #Accediendo al objeto
        self.object = self.get_object
        #Realizando queryset para encontrar el ID del usuario
        user_id = User.objects.get(id=User.objects.filter(username=self.request.user))

        #Extrayendo informacion del formulario (Solamente el campo text)
        form = self.form_class(request.POST)

        #Verificando si la informacion del formulario es valida
        if form.is_valid():
            #Asignando informacion a variable valor
            valor = form.save(commit=False)
            #Asignando llave foranea igualando a el queryset del usuario
            valor.user_twit = user_id
            valor.date_twit = datetime.now()
            #Guardando la informacion en la base de datos
            valor.save()
            #Redireccionando informacion
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, error='1'))

