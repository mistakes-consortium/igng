from django.conf import settings
import os
from pilkit.utils import suggest_extension
import shortuuid


def generate_file_name(generator, sourcename):
    return "%s_%s" % (
        # shortuuid.uuid(),
        sourcename.split('.')[0],
        generator.options.get('prefix'),
    )


def igng_source_name_as_path(generator):
    """
    A namer that will give us slightly smaller than the default filename.
    literally identical to 'imagekit.cachefiles.namers.source_name_as_path'
    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        directory = settings.IMAGEKIT_CACHEFILE_DIR

    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        directory = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR, os.path.splitext(source_filename)[0])

    ext = suggest_extension(source_filename or "", generator.format)

    # generate a better filename

    joined = os.path.normpath(os.path.join(directory, '%s%s' % (generate_file_name(generator, source_filename), ext)))
    return joined