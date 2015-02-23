from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


def home(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('aviastudent_templates/home.html',
                              context_instance=context)


@login_required
def test_auth_required(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('aviastudent_templates/test_auth_required.html',
                              context_instance=context)
