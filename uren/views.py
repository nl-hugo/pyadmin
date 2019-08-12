from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.views import generic

from uren.models import ProjectHours


class UrenListView(generic.ListView):
    model = ProjectHours
    context_object_name = 'hours'
    template_name = 'uren/uren.html'

    # uren per maand, per activiteit, per project, per klant
    def get_queryset(self):
        return ProjectHours.objects.annotate(month=TruncMonth('date')).values(
            'month', 'project__name', 'project__client__name').annotate(
            sum=Sum('hours'), count=Count('id'))
