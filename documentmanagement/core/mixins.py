from django.db import models

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modified At')

    class Meta:
        abstract = True
        ordering = ['-created_at', '-modified_at']
        verbose_name = 'Timestamped Model'
        verbose_name_plural = 'Timestamped Models'

class ResponseMixi:
    def format_response(self, data, message="Success", status_code=200):
        return {
            "status": status_code,
            "message": message,
            "data": data
        }