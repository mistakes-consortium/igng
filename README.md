# i.GNG

It's an image gallery that wont log you out randomly.

## TODO

### Features

- users featured imgs
- single image view / lightbox
- delete images/galleries
- short/long term permalinks

### Stuff 

- Do something with tags
- Expose EXIF
- Moderate Brandability
- Better Admin
- API Serializers
- API Endpoints
- More Empty Gallery Images
- Bulk uploads

## Done

### features

- basic admin
- unix timestamps
- exif extraction
- no logoutz
- tags
- uploads
- allauth ( persona for @wcummings )
- make all form features work [crispy-forms-materialize + django-crispy-forms]
- upload to gallery
- bbcode generator

### Stuff

- Frontend
- Models
- EXIF Extraction
- Image/Gallery Serializers
- Image/Gallery Endpoints


#### NOTES

- SITE_URL needs to be set in local_settings for bbcode and other generators to work properly

- apt-get install libfreeimage-dev (else stuff becomes sad)