from .models import Twitts
# Create your views here.

#Vista que retornara los Twitts realizados por el usuario dado
def Tview(user):
    #Realizando QuerySet y ordenando este de forma Desendente con la fecha
    data = Twitts.objects.filter(user_twit_id=user.id).order_by('-date_twit')
    return data


