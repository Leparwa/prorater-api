from django.db import models
from django.conf import settings
def project_upload(instance, filename):
    return 'project_image/{}/{}'.format(instance.user_id, filename)
class Review(models.Model):
    design = models.CharField(max_length=100)
    usability = models.CharField(max_length=100)
    content= models.CharField(max_length=100)
class Project(models.Model):
    project_image = models.ImageField(upload_to=project_upload)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    reviews = models.ForeignKey(Review, models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return '%d: %s' % (self.description, self.title)