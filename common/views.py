from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext

from common.forms import ProfileUIForm


@login_required
def user_settings(request):
    return render(request, "settings.html", {})

@login_required
def user_settings_ui(request):
    context = {}
    if request.method == 'POST':
        form = ProfileUIForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("usersettings")
    else:
        form = ProfileUIForm(instance=request.user.profile)

    context['form'] = form
    return render(request, "form_generic.html", context)