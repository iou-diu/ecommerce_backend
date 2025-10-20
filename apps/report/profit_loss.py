from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProfitLossReportView(LoginRequiredMixin, TemplateView):
    """
    View for displaying purchase and sale report with custom date range support.
    """
    template_name = 'reports/profit_loss.html'
