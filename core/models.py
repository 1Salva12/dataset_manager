from django.db import models

class Dataset(models.Model):
    id = models.BigAutoField(primary_key=True)  # ID explícito para evitar warnings
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notebook(models.Model):
    id = models.BigAutoField(primary_key=True)  # ID explícito para evitar warnings
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
