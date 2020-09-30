from django.db import models



class Course(models.Model):

## ceci est le model de base de Activity dans 0.7.* AVEC quelques ajouts ;)

"""
    name = models.CharField(max_length=255, null=False) # this is the moodle/LTI name 
    platonname= models.CharField(max_length=255, null=True) # used in display if null use name
    open = models.BooleanField(default=True) # accessible 
    hidden = models.BooleanField(default=True) # visible by teachers only 
    activity_type = models.CharField(max_length=30, null=False,
                                     choices=zip(type_dict.keys(), type_dict.keys()))
    activity_data = JSONField(default=dict)
    # this is for the tree structure 
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    # this is for the "la classe" strtucture 
    course = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    teacher = models.ManyToManyField(User, related_name="teaches", blank=True)
    student = models.ManyToManyField(User, related_name="learn", blank=True)
    pl = models.ManyToManyField(PL, through="PLPosition")
    # Those are here to store data for stats 
    stat_data = JSONField(default=dict)
    stat_timestamp = models.DateTimeField()

"""

# doit contenir les stats du cours dans un json field avec un système de cache
# rafraichissement toutes les heures (seulement) 
# Quand c'est indiqué RECURSIF c'est défini a chaque niveau et calculer avec un opérateur en général sum 
# Stats GLobales :
#    nbhits : nombre d'answer du cours (tous les "validate" sans erreur), RECURSIF (sum)
#    nbexos: nombre d'exercices, RECURSIF(sum)
#    avghits: (nbhits//nbstudents) du cours,RECURSIF(None) 
#    nbstudents : len(course.students())
# Stats per student per group: 
#    maxpl (PL): note max sur un pl pour un élève 
#    meanpl: note moyenne sur un pl pour un élève (donne une indication sur le nombre d'essais nécessaires).  
#    maxpl (PLTP): somme des maxpl pour un élève 
#    meanpl(PLTP): moyenne des maxpl des pl du pltp 
#    avgavg: moyenne des moyenne des sous activités, RECURSIF(mean), mean is define as sum//number of sub activities
#    avgmax: Moyenne des grade max sur l'ensemble des étudiants 
#    grademax: note maximale des PL (pour les activités la somme des grademax des sous activités RECURSIF)
#    timetotal: somme de tout le temps consomé par les utilisateurs sur ce cours, RECUSIF(sum) 
#    
# Stats semi globales: necessité de calculer les stats de chaque élève pour avoir les stats globales.





