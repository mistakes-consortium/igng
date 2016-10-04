## LAPSES
import os
import shortuuid
from celery import shared_task
from django.conf import settings
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

from images.models import Gallery, Image
from lapses.models import AutoLapseInstance, LapseInstanceStatus, AutoLapseInstanceFile, video_mp4_name_generator, \
    video_webm_name_generator, gif_name_generator, target_path_generator


@shared_task
def autolapse(gallery_id, force=False):
    print "WEW"
    g = Gallery.objects.get(pk=gallery_id)
    icnt = g.images.count()
    lapses = g.autolapse_configs.filter(enabled=True)
    for l in lapses:
        if icnt % l.create_new_every != 0 and not force:
            continue
        print "YAY"
        lapse_instance = AutoLapseInstance(configuration=l, status=LapseInstanceStatus.PENDING)
        lapse_instance.save()

        image_object_list = g.images.order_by('-uploaded')[0:l.image_count]
        max_size = l.max_output_size.value
        sizes_to_do = Image.AVAIL_SIZES[max_size:]
        sizes_to_do_as_ints = Image.AVAIL_INTS[max_size:]
        clips = {}

        lapse_instance.status=LapseInstanceStatus.WORKING
        lapse_instance.save()
        print lapse_instance.uuid

        for size,index in zip(sizes_to_do,sizes_to_do_as_ints):
            image_file_list = [str(getattr(i, size).path) for i in image_object_list ] #forcing str moviepy/issues/293
            # print image_file_list
            clip = ImageSequenceClip(image_file_list, fps=l.frames_per_second)
            uuid = shortuuid.uuid()

            alfile = AutoLapseInstanceFile.objects.create(instance=lapse_instance, output_size=index, uuid=uuid)
            path_prefix = target_path_generator(alfile, prefix=settings.MEDIA_ROOT)
            if not os.path.exists(path_prefix):
                os.makedirs(path_prefix)
            print path_prefix
            clip.write_videofile(video_mp4_name_generator(alfile, prefix=settings.MEDIA_ROOT))
            clip.write_videofile(video_webm_name_generator(alfile, prefix=settings.MEDIA_ROOT))
            clip.write_gif(gif_name_generator(alfile, prefix=settings.MEDIA_ROOT))

            alfile.file_video_mp4 = video_mp4_name_generator(alfile)
            alfile.file_video_webm = video_webm_name_generator(alfile)
            alfile.file_video_gif = gif_name_generator(alfile)

            alfile.save()


