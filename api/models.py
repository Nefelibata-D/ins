import os.path

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings


class ShortPath(models.Model):
    id = models.AutoField(primary_key=True)
    shortcode = models.CharField('短链接', max_length=15)
    name = models.CharField('文件名', max_length=20)
    download_url = models.TextField('服务器下载链接')
    file_path = models.FileField(verbose_name='服务器路径', null=True, blank=True)
    time = models.DateTimeField('处理时间')

    def __str__(self):
        return str(self.id)


@receiver(pre_delete, sender=ShortPath)
def shortpath_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    files = getattr(instance, 'file_path', '')
    if not files:
        return
    file_to_delete = os.path.join(settings.MEDIA_ROOT, str(files.path))
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
