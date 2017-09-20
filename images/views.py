from copy import copy
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context import RequestContext
from taggit.models import Tag, TaggedItem

from images.forms import ImageUploadForm, GallerySettingsForm, GalleryCreateForm, ImageSettingsForm, \
    ImageSettingsTagForm, UserSettingsImageGalleryForm
from images.models import Image, Gallery


def index(request):
    return render(request, "index.html", {})


# user facing views
@login_required
def upload(request, gallery_uuid=None):
    context = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # fill some stuff
            if not gallery_uuid:
                gallery = request.user.galleries.get(title="Default")
            else:
                galleries = Gallery.objects.notdefault(user=request.user)
                gallery = get_object_or_404(galleries, uuid=gallery_uuid)

            obj = form.save(commit=False)
            obj.gallery = gallery
            obj.user = request.user
            obj.save()
            form.save_m2m()  # fix for missing tags
            return redirect("upload_success", obj_uuid=obj.uuid)
    else:
        form = ImageUploadForm()

    context['form'] = form
    return render(request, "upload.html", context)


@login_required
def upload_success(request, obj_uuid):
    context = {}
    object = get_object_or_404(Image, uuid=obj_uuid)
    context['object'] = object
    return render(request, "upload_success.html", context)


# sharable
def image_detail(request, obj_uuid):
    context = {}
    object = get_object_or_404(Image, uuid=obj_uuid)
    context['object'] = object
    context['obj_next'] = object.get_next_by_gallery_ordering()
    context['obj_prev'] = object.get_prev_by_gallery_ordering()

    ui_override = request.GET.get("ui", None)
    context['ui_override'] = None

    available = []
    for k, v in object.view_flags.iteritems():
        if v:
            available.append(k)
    context['available'] = available

    if ui_override in object.view_flags.keys():
        context['ui_override'] = ui_override

    elif ui_override and object.view_flags.mask != 0:
        if ui_override in available:
            context['ui_override'] = ui_override

    elif object.view_flags.mask != 0:
        context['ui_override'] = available[0]

    else:
        pass

    return render(request, "image_detail.html", context)


@login_required
def user_default_gallery_images(request):
    gallery = request.user.galleries.default(request.user)
    images = gallery.images.all().prefetch_related('tags').order_by(*gallery.display_sort_string)

    paginator = Paginator(images, 12)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        imgs = paginator.page(1)
    except EmptyPage:
        imgs = paginator.page(paginator.num_pages)
    context = {
        "images": imgs,
        "gallery": gallery,
        "is_default_gallery": True,
    }
    return render(request, 'image_list.html', context)


@login_required
def user_create_gallery(request):
    context = {}
    if request.method == 'POST':
        form = GalleryCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            # fill some stuff
            obj.user = request.user
            obj.save()
            return redirect("user_galleries")
    else:
        form = GalleryCreateForm()

    context['form'] = form
    return render(request, "gallery_settings.html", context)


@login_required
def user_get_gallery_images(request, obj_uuid):
    gallery = get_object_or_404(Gallery, uuid=obj_uuid)
    images = gallery.images.all().order_by(*gallery.display_sort_string)

    paginator = Paginator(images, gallery.gallery_pagination_count)

    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        imgs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        imgs = paginator.page(paginator.num_pages)

    context = {
        "images": imgs,
        "gallery_name": gallery.title,
        "gallery": gallery,
        "is_users_gallery": True,
    }
    return render(request, 'image_list.html', context)


@login_required
def user_galleries(request):
    galleries = request.user.galleries.notdefault(request.user).prefetch_related("images")

    paginator = Paginator(galleries, 12)
    page = request.GET.get('page')
    try:
        gals = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gals = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gals = paginator.page(paginator.num_pages)

    context = {"galleries": gals}
    return render(request, "gallery_list.html", context)


@login_required
def user_gallery_priv_toggle(request, obj_uuid):
    galleries = request.user.galleries.notdefault(request.user)
    gallery = get_object_or_404(galleries, uuid=obj_uuid)

    gallery.private = not gallery.private
    gallery.save()

    return redirect("user_galleries")


@login_required
def user_gallery_settings(request, obj_uuid):
    galleries = request.user.galleries.notdefault(request.user)
    gallery = get_object_or_404(galleries, uuid=obj_uuid)

    context = {}
    if request.method == 'POST':
        form = GallerySettingsForm(request.POST, instance=gallery)
        if form.is_valid():
            obj = form.save()
            target = request.GET.get("ret", 0)
            if target == "1":
                return redirect("user_gallery_images", obj_uuid=obj.uuid)
            return redirect("user_galleries")
    else:
        form = GallerySettingsForm(instance=gallery)

    context['form'] = form
    context['gallery'] = gallery

    return render(request, "gallery_settings.html", context)


# look into CBVs here
def gallery_tooltip_info_view(request, obj_uuid=None):
    images = Image.objects.filter(
        Q(gallery__private=False) | Q(gallery__user=request.user)
    )
    image = get_object_or_404(images, uuid=obj_uuid)

    context = {}
    context['image'] = image
    return render(request, "ajax_lapse.html", context)


def gallery_exif_info_view(request, obj_uuid=None):
    images = Image.objects.filter(
        Q(gallery__private=False) | Q(gallery__user=request.user)
    )
    image = get_object_or_404(images, uuid=obj_uuid)

    context = {}
    context['exif'] = image.exif_data.values_list('key__key', 'value__value')
    return render(request, "ajax_exif.html", context)


# potentially external views
def linked_gallery_view(request, obj_uuid):
    """
    View For Permalinks
    """
    gallery = get_object_or_404(Gallery, uuid=obj_uuid)
    images = gallery.images.all().order_by(*gallery.display_sort_string)

    paginator = Paginator(images, gallery.gallery_pagination_count)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        imgs = paginator.page(1)
    except EmptyPage:
        imgs = paginator.page(paginator.num_pages)
    context = {
        "images": imgs,
        "gallery": gallery,
        "gallery_name": gallery.title
    }
    return render(request, 'image_list.html', context)


# tag views
@login_required
def tags_user_all(request):
    context = {}

    user = request.user
    # ct = ContentType.objects.get_for_model(Image)
    # TaggedItem.objects.filter(content_type=ct, content_object__user=user)
    imgs = Image.objects.filter(user=user).values_list('pk', flat=True)
    tags = Tag.objects.filter(image__in=imgs).distinct()

    context['tags'] = tags
    context['gallery_name'] = False
    return render(request, "taglist.html", context)


@login_required
def tags_user_detail(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    # see user_default_gallery_images()
    imgs = Image.objects.filter(user=request.user, tags__name=tag).prefetch_related('tags')

    paginator = Paginator(imgs, 12)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        imgs = paginator.page(1)
    except EmptyPage:
        imgs = paginator.page(paginator.num_pages)
    context = {
        "images": imgs,
        "gallery": Gallery.objects.first(),
        "is_default_gallery": True,
        "gallery_name": "tag <b>%s</b>" % (tag.name,),
    }
    return render(request, 'image_list.html', context)


def tags_gallery_all(request, obj_uuid):
    context = {}

    gallery = get_object_or_404(Gallery, uuid=obj_uuid)
    imgs = gallery.images.all().values_list('pk', flat=True)
    tags = Tag.objects.filter(image__in=imgs).distinct()

    context['tags'] = tags
    context['gallery_name'] = gallery
    return render(request, "taglist.html", context)


def tags_gallery_detail(request, obj_uuid, tag):  # look into CBVs for the gallery image listings...
    tag = get_object_or_404(Tag, name=tag)
    gallery = get_object_or_404(Gallery, uuid=obj_uuid)
    imgs = Image.objects.filter(tags__name=tag, gallery=gallery).prefetch_related('tags')
    paginator = Paginator(imgs, 12)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        imgs = paginator.page(1)
    except EmptyPage:
        imgs = paginator.page(paginator.num_pages)

    if request.user == gallery.user:
        gallery_name = "tag <b>%s</b> under gallery <a href=\"%s\">%s</a> - <a href=\"%s\" class=\"purple-text accent-1\">All Tag Instances</a>" % (
            tag.name,
            reverse_lazy("user_gallery_images", args=[gallery.uuid]),
            gallery.title,
            reverse_lazy("tags_user_detail", args=[tag.name]),
        )
    else:
        gallery_name = "tag <b>%s</b> under gallery <a href=\"%s\">%s</a>" % (
            tag.name,
            reverse_lazy("user_gallery_images", args=[gallery.uuid]),
            gallery.title
        )
    context = {
        "images": imgs,
        "gallery": gallery,
        "is_default_gallery": True,
        "gallery_name": gallery_name
    }

    return render(request, 'image_list.html', context)


@login_required
def user_image_settings(request, obj_uuid):
    """
    This one won't be as pretty as the ones below
    :param request:
    :param obj_uuid:
    :return:
    """
    queryset = Image.objects.filter(user=request.user)
    image = get_object_or_404(queryset, uuid=obj_uuid)
    context = {}

    if request.method == 'POST':
        form = ImageSettingsForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect("image_detail", obj_uuid=image.uuid)
    else:
        form = ImageSettingsForm(instance=image)

    context['form'] = form
    context['custom_title'] = "Change Image"
    return render(request, "upload.html", context)


@login_required
def user_image_tags(request, obj_uuid):
    queryset = Image.objects.filter(user=request.user)
    image = get_object_or_404(queryset, uuid=obj_uuid)

    context = {}

    if request.method == 'POST':
        form = ImageSettingsTagForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect("image_detail", obj_uuid=image.uuid)
    else:
        form = ImageSettingsTagForm(instance=image)

    context['form'] = form
    context['custom_title'] = "Change Image"
    context['template_tagging'] = True
    return render(request, "upload.html", context)

@login_required
def user_image_gallery_move(request, obj_uuid):
    queryset = Image.objects.filter(user=request.user)
    image = get_object_or_404(queryset, uuid=obj_uuid)
    old = copy(image.gallery.uuid) # yay!
    context = {}

    if request.method == 'POST':
        form = UserSettingsImageGalleryForm(request.POST, instance=image, user=request.user)
        if form.is_valid():
            new_instance = form.save(commit=False)

            new = new_instance.gallery.uuid
            print(old,new)
            # return render(request, "upload.html", context)
            return redirect("image_settings_gallery_move_do", obj_uuid=image.uuid, gallery_from=old, gallery_to=new)
    else:
        form = UserSettingsImageGalleryForm(instance=image, user=request.user)

    context['form'] = form
    context['custom_title'] = "Change Image"
    return render(request, "upload.html", context)

@login_required
def user_image_gallery_move_do(request, obj_uuid, gallery_from, gallery_to):
    queryset = Image.objects.filter(user=request.user)
    image = get_object_or_404(queryset, uuid=obj_uuid)
    # print(image.gallery.uuid)

    g_qs = Gallery.objects.filter(user=request.user)
    gallery_to_o = get_object_or_404(g_qs, uuid=gallery_to)
    gallery_from_o = get_object_or_404(g_qs, uuid=gallery_from)

    if gallery_from == gallery_to:
        return redirect("image_detail", obj_uuid=obj_uuid)

    if image.gallery.uuid == gallery_to:
        pass
        print("same")
    elif image.gallery.uuid == gallery_from:
        image.gallery = gallery_to_o
        image.save()
        print("moving")
    context = {"object":image, "to": gallery_to, "from": gallery_from, "from_title":gallery_from_o.title}
    return render(request, "gallery_move.html", context)
