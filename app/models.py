from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Dokumen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_file = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    filenya = models.FileField(upload_to='dokumen/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.nama_file

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

