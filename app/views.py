from django.shortcuts import render, render_to_response
from django.template import RequestContext

def error403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response

def error400(request):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response
