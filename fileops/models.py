from django.db import models

# Create your models here.


class Upload(models.Model):
    temp_id = models.CharField(max_length=100)
    doc = models.FileField(upload_to='files')
