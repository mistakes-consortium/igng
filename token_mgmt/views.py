from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

# Create your views here.
from django.template.context import RequestContext
from rest_framework.authtoken.models import Token

@login_required
def token_mgmt_basic_list(request):
    tokens = Token.objects.filter(user=request.user)
    context = {'tokens':tokens}
    return render(request, 'tokens/token_list.html', context)

@login_required
def token_mgmt_basic_create(request):
    t,c = Token.objects.get_or_create(user=request.user)
    if c:
        messages.info(request, "Token Added")
    # return render(request, 'tokens/token_list.html', {)
    return redirect('token_list')


@login_required
def token_mgmt_basic_remove(request, id):
    qs = Token.objects.filter(user=request.user)
    t = get_object_or_404(qs, pk=id)

    t.delete()
    messages.info(request, "Token Removed")

    # return render(request, 'tokens/token_list.html', {)
    return redirect('token_list')