from django.db import models



class Course(models.Model):
    pass

# doit contenir les stats du cours dans un json field avec un système de cache
# rafraichissement toutes les heures (seulement) 
# Stats :
#    nbhits : nombre d'answer du cours (tous les validate)
#    avghits: nbhiots //nbstudents
#    nbstudents : len(students())
#    nbhitsperPltp :
