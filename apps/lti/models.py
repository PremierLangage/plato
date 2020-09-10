from django.contrib.auth.models import User
from django.db import models



class LMS(models.Model):
    name = models.TextField()
    guid = models.TextField(unique=True)
    url = models.URLField(null=False)
    outcome_url = models.URLField(null=False)
    client_id = models.TextField()
    client_secret = models.TextField()



class LTIUser(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    lms = models.ForeignKey(LMS, null=False, on_delete=models.CASCADE)
    user_lms_guid = models.TextField(unique=True)



class LTICourse(models.Model):
    lms = models.ForeignKey(LMS, null=False, on_delete=models.CASCADE)
    course_lms_guid = models.TextField(unique=True)



class LTICourseAbstract(models.Model):
    lti: models.ForeignKey(LTICourse, null=True, default=None, blank=True,
                           on_delete=models.SET_NULL)
    
    
    class Meta:
        abstract = True
