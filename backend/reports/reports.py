from slick_reporting.views import ReportView
from slick_reporting.fields import SlickReportField
from salon.models import service
from django.db.models import Count, Sum

class ServiceReport(ReportView):
    report_model = service
    date_field = 'createdAt'
    default_report = 'show_empty'

    group_by = 'category'

    columns = [
        'category',
        SlickReportField.create(Sum, 'price', name='total_price', verbose_name='Total Price'),
        SlickReportField.create(Count, 'id', name='service_count', verbose_name='Number of Services'),
    ]

    template_name = 'slick_reporting/services_reports.html'


class ServiceGivenReport(ReportView):
    pass