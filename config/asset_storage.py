from storages.backends.s3boto3 import S3Boto3Storage
class MediaStorage(S3Boto3Storage):
    location = 'media/'
    bucket_name = 'fastercampusmedia.jonus.co.kr'
    custom_domain = 'fastercampusmedia.jonus.co.kr'
    file_overwrite = False