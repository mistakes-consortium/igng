from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

# Create your views here.
from django.template.context import RequestContext
from rest_framework.authtoken.models import Token


def token_mgmt_basic_list(request):
    tokens = Token.objects.filter(user=request.user)
    context = {'tokens':tokens}
    context = RequestContext(request, context)
    return render_to_response('tokens/token_list.html', context)


def token_mgmt_basic_create(request):
    t,c = Token.objects.get_or_create(user=request.user)
    if c:
        messages.info(request, "Token Added")
    context = RequestContext(request, {"tokens":[t]})
    # return render_to_response('tokens/token_list.html', context)
    return redirect('token_list')


def token_mgmt_basic_remove(request, id):
    t = get_object_or_404(Token, pk=id)
    if t.user != request.user:
        raise Http404()

    t.delete()
    messages.info(request, "Token Removed")
    context = RequestContext(request, {})
    # return render_to_response('tokens/token_list.html', context)
    return redirect('token_list')