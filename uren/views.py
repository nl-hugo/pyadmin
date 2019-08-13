from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.views import generic

from uren.models import ProjectHours


class UrenListView(generic.ListView):
    model = ProjectHours
    context_object_name = 'hours'
    template_name = 'uren/uren.html'

    # TODO: dit is eigenlijk al een factuur specificatie...
    def get_queryset(self):
        return ProjectHours.objects.annotate(
            month=TruncMonth('date'), amount=F('activity__price') * F('hours'), vat=F('amount') * F('activity__vat'),
            total=F('amount') + F('vat')
        ).values(
            'month', 'project__name', 'project__client__name', 'activity__description'
        ).annotate(
            sum=Sum('hours'), amount=Sum('amount'), vat=Sum('vat'), total=Sum('total')
        ).order_by(
            'month', 'project__client__name', 'project__name', 'activity__description'
        )
