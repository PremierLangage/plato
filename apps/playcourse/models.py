from django.db import models



class Course(models.Model):
    pass

# doit contenir les stats du cours dans un json field avec un système de cache
# rafraichissement toutes les heures (seulement) 
# Stats :
#    nbhits : nombre d'answer du cours (tous les "validate" sans erreur), RECURSIF
#    nbexos: nombre d'exercices, RECURSIF 
#    avghits: (nbhits//nbstudents) du cours
#    nbstudents : len(course.students())
#    avgavg: moyenne des moyenne des sous activités 
#    avgmax: Moyenne des grade max 
#    
