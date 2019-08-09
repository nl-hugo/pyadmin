from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
        related_name='projects')

    def __str__(self):
        return '{} - {}'.format(self.client.name, self.name)


class ProjectHours(models.Model):
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.PROTECT,
        related_name='project_hours')
