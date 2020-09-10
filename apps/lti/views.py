from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST



@require_POST
def course(request: HttpRequest) -> HttpResponse:
    data = request.POST
    # TODO lti redirection to course
    return HttpResponseRedirect(reverse("playcourse:get_course", args=[course.id]))
