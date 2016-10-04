from django.db import models
from django_extensions.db.fields import ShortUUIDField
from enumfields import EnumIntegerField, Enum

# lapse models
class AutoLapseOutputSizes(Enum):
    ORIGINAL = 0
    BIGGISH = 1
    DEFAULT = 2
    PREVIEW = 3
    # have these be auto-genned anyway?
    THUMB = 4
    THINYTHUMB = 5


class LapseInstanceStatus(Enum):
    PENDING = 0
    WORKING = 1
    COMPLETED = 2


class AutoLapseConfiguration(models.Model):
    uuid = ShortUUIDField(db_index=True)

    create_new_every = models.IntegerField(help_text="How many uploads until we automatically generate a lapse")
    source_gallery = models.ForeignKey("images.Gallery", related_name="autolapse_configs")
    image_count = models.IntegerField(help_text="How many images maximum to lapse")
    frames_per_second = models.IntegerField(help_text="FPS of the resulting video")
    enabled = models.BooleanField()
    max_output_size = EnumIntegerField(AutoLapseOutputSizes, help_text="Biggest size we generate")


class AutoLapseInstance(models.Model):
    class Meta:
        get_latest_by = "created"

    created = models.DateTimeField(auto_now_add=True)
    uuid = ShortUUIDField(db_index=True)

    configuration = models.ForeignKey("AutoLapseConfiguration", related_name="autolapse_instances")
    status = EnumIntegerField(LapseInstanceStatus)

    @property
    def preview(self):
        return self.autolapse_files.filter(output_size=3).get()


def file_name_generator(instance, filename):
    return "%(gallery)s/%(lapseconfig)s/%(date)s_%(id)s_%(outsize)s" % {
        "gallery": instance.instance.configuration.source_gallery.uuid,
        "lapseconfig": instance.instance.configuration.uuid,
        "date": instance.created.date(),
        "id": instance.instance.uuid,
        "outsize": instance.output_size
    }

def target_path_generator(instance, prefix=""):
    return prefix + "%(gallery)s/%(lapseconfig)s/" % {
        "gallery": instance.instance.configuration.source_gallery.uuid,
        "lapseconfig": instance.instance.configuration.uuid,
    }


def video_mp4_name_generator(instance=None, filename=None, prefix=""):
    return prefix + file_name_generator(instance, filename) + ".mp4"


def video_webm_name_generator(instance=None, filename=None, prefix=""):
    return prefix + file_name_generator(instance, filename) + ".webm"


def gif_name_generator(instance=None, filename=None, prefix=""):
    return prefix + file_name_generator(instance, filename) + ".gif"

class AutoLapseInstanceFile(models.Model):
    uuid = ShortUUIDField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    instance = models.ForeignKey("AutoLapseInstance", related_name="autolapse_files")
    output_size = EnumIntegerField(AutoLapseOutputSizes)
    file_video_mp4 = models.FileField(upload_to=video_mp4_name_generator, max_length=512)
    file_video_webm = models.FileField(upload_to=video_webm_name_generator, max_length=512)
    file_video_gif = models.ImageField(upload_to=gif_name_generator, max_length=512)

from lapses.signals import do_the_lapse_hook