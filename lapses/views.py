from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

# Create your views here.
from django.template.context import RequestContext

from images.models import Gallery
from lapses.forms import LapseCreateForm
from lapses.models import AutoLapseInstance, AutoLapseConfiguration
from lapses.tasks import autolapse


@login_required
def mk_lapse(request, gal_uuid):
    gallery_qs = request.user.galleries.all()
    g = get_object_or_404(gallery_qs, uuid=gal_uuid)
    context = {}
    if request.method == 'POST':
        form = LapseCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.source_gallery = g
            # fill some stuff
            obj.user = request.user
            obj.save()
            autolapse(g.pk, force=True)
            return redirect("lapse_get", obj_uuid=obj.uuid)
    else:
        form = LapseCreateForm()
    context['form'] = form
    context = RequestContext(request, context)
    return render(request, "gallery_settings.html", context)

def update_lapse(request, obj_uuid):
    galleries = request.user.galleries.all()
    qs = AutoLapseConfiguration.objects.filter(source_gallery__in=galleries)
    lapse = get_object_or_404(qs, uuid=obj_uuid)

    context = {}
    if request.method == 'POST':
        form = LapseCreateForm(request.POST, instance=lapse)
        if form.is_valid():
            obj = form.save()
            return redirect("lapse_get", obj_uuid=obj.uuid)
    else:
        form = LapseCreateForm(instance=lapse)
    context['form'] = form
    context = RequestContext(request, context)

    return render(request, "gallery_settings.html", context)

def get_lapse(request, obj_uuid):
    context = {}
    config = get_object_or_404(AutoLapseConfiguration, uuid=obj_uuid)
    latest = config.autolapse_instances.latest()
    context['latest'] = latest
    context = RequestContext(request, context)
    return render(request, "lapse_detail.html", context=context)