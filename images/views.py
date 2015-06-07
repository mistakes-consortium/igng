import base64
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

# Create your views here.
from django.template.context import RequestContext
from images.forms import ImageUploadForm
from images.models import Image, Gallery


def index(request):
    context = RequestContext(request)
    return render_to_response("index.html", context)


def upload(request):
    context = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            # fill some stuff
            gallery = request.user.galleries.get(title="Default")
            obj.gallery = gallery
            obj.user = request.user
            obj.save()
            return redirect("upload_success", obj_uuid=obj.uuid)
    else:
        form = ImageUploadForm()

    context['form'] = form
    context = RequestContext(request, context)
    return render(request, "upload.html", context)


def upload_success(request, obj_uuid):
    context = {}
    object = get_object_or_404(Image, uuid=obj_uuid)
    context['object'] = object
    context = RequestContext(request, context)
    return render(request, "upload_success.html", context)

@login_required
def user_default_gallery_images(request):
    gallery = request.user.galleries.default(request.user)
    images = gallery.images.all()

    paginator = Paginator(images, 12)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        imgs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        imgs = paginator.page(paginator.num_pages)

    context = RequestContext(request, {"images": imgs})
    return render_to_response('image_list.html', context)

@login_required
def user_get_gallery_images(request, obj_uuid):
    gallery = get_object_or_404(Gallery, uuid=obj_uuid)
    images = gallery.images.all()

    paginator = Paginator(images, 12)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        imgs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        imgs = paginator.page(paginator.num_pages)

    context = RequestContext(request, {"images": imgs, "gallery_name":gallery.title})
    return render_to_response('image_list.html', context)


@login_required
def user_galleries(request):
    galleries = request.user.galleries.notdefault(request.user)

    context = RequestContext(request,{"galleries":galleries})
    return render_to_response("gallery_list.html", context)

@login_required
def user_settings(request):
    context = RequestContext(request)
    return render_to_response("settings.html", context)