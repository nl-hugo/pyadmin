from django.db import models


def get_default_km_activity():
    return Activity.objects.filter(is_billable=False, unit__code='KM').first()


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='projects')

    def __str__(self):
        return '{} - {}'.format(self.client.name, self.name)


class Unit(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']


class Activity(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True, related_name='units')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vat = models.DecimalField(max_digits=3, decimal_places=2, default=0.21)
    is_billable = models.BooleanField(default=False)

    def __str__(self):
        return '({}) {}'.format(self.code, self.description)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Activities'


class ProjectHours(models.Model):
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='project')
    activity = models.ForeignKey('Activity', on_delete=models.PROTECT, null=True, related_name='activity')

    def __str__(self):
        return '{} - {}'.format(self.date, self.activity)

    class Meta:
        ordering = ['-date', 'project', 'activity']
        verbose_name_plural = 'Project hours'
