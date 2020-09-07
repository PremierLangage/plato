from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from playactivity.models import Activity
from playexo.models import Answer, LoggedPLSession

# creation des modèles stockant les valeurs calculées
#
# a partir des valeurs de answers dans playexo

class ActivityStats:
    pla_id = models.ForeignKey(Activity)


@receiver(post_save, sender=Answer)
def answerhook(sender , instance: Answer , created, *args, **kwargs):

    if type(instance.session) != LoggedPLSession :
            print(" rien a battre ")

    plid=    instance.session.pl_id
    userid= instance.session.pl_id
