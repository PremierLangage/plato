from django.db import models
from django.db.models.signals import post_save 
from django.dispatch import receiver 
# Create your models here.



# creation des modèles stockant les valeurs calculées a partir des valeurs de answers dans playexo
from playexo.models import Answer


@receiver(post_save,sender=Answer)
def answerhook(sender , instance: Answer , created, *args, **kwargs):

    print("Answer created")

    raise(False)
