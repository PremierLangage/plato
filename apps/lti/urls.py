from django.urls import path
from lti import views


app_name = 'lti'

urlpatterns = [
    path(r'', views.course, name="course"),
]
