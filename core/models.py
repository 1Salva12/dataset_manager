from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notebook(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='notebooks'
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='notebooks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
