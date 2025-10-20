from django.db.models import Sum, F, Q, DecimalField, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.inventory.models import PurchaseOrderItem


def get_date_range(date_filter, start_date_str=None, end_date_str=None):
    """
    Get date range based on filter or custom dates.
    """
    today = timezone.now().date()

    # Handle custom date range
    if date_filter == 'custom' and start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            return start_date, end_date
        except (ValueError, TypeError):
            # Fall back to today if date parsing fails
            return today, today

    # Handle predefined date ranges
    if date_filter == 'today':
        start_date = today
        end_date = today
    elif date_filter == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif date_filter == 'last_7_days':
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_filter == 'last_30_days':
        start_date = today - timedelta(days=30)
        end_date = today
    elif date_filter == 'this_month':
        start_date = today.replace(day=1)
        end_date = today
    elif date_filter == 'last_month':
        last_month = today.replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1)
        end_date = last_month
    elif date_filter == 'this_year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif date_filter == 'last_year':
        last_year = today.year - 1
        start_date = today.replace(year=last_year, month=1, day=1)
        end_date = today.replace(year=last_year, month=12, day=31)
    else:  # Default to current financial year
        if today.month < 4:  # If current month is before April
            start_date = today.replace(year=today.year - 1, month=4, day=1)
        else:
            start_date = today.replace(month=4, day=1)
        end_date = today

    return start_date, end_date


def calculate_purchase_metrics(start_date, end_date, location=None):
    """
    Calculate purchase metrics for given date range and location.
    Handles both global purchase tax and inline item taxes.
    """
    from apps.inventory.models import PurchaseOrder, PurchaseOrderItem
    from django.db.models import Case, When, F, Value

    # Base query for purchases
    purchase_query = Q(
        order_date__date__range=(start_date, end_date),
        status__in=['ordered', 'received', 'delivered']
    )

    # Base query for purchase items
    purchase_item_query = Q(
        purchase_order__order_date__date__range=(start_date, end_date),
        purchase_order__status__in=['ordered', 'received', 'delivered']
    )

    # Get purchase orders and items
    purchase_list = PurchaseOrder.objects.filter(purchase_query)
    item_list = PurchaseOrderItem.objects.filter(purchase_item_query)

    # Calculate total purchase amount
    total_purchase = purchase_list.aggregate(
        total_purchase=Sum('final_total_cost', output_field=DecimalField())
    )['total_purchase'] or Decimal('0.0')

    # Calculate global purchase tax
    total_purchase_tax = purchase_list.annotate(
        tax_amount=Case(
            When(
                purchase_tax_type='percentage',
                then=F('final_total_cost') * F('purchase_tax_value') / 100
            ),
            When(
                purchase_tax_type='flat',
                then=F('purchase_tax_value')
            ),
            default=Value(0),
            output_field=DecimalField()
        )
    ).aggregate(
        total_tax=Sum('tax_amount')
    )['total_tax'] or Decimal('0.0')

    # Calculate inline item taxes
    inline_purchase_tax = item_list.aggregate(
        total_tax=Sum('tax', output_field=DecimalField())
    )['total_tax'] or Decimal('0.0')

    # Calculate total tax (global + inline)
    total_tax = total_purchase_tax + inline_purchase_tax

    # Calculate purchase due amount
    purchase_due = (
            purchase_list.annotate(
                amount_paid=Subquery(
                    PurchaseOrder.objects.filter(
                        pk=OuterRef('pk')
                    ).annotate(
                        paid=Sum('purchaseorderpayments__amount',
                                 filter=Q(purchaseorderpayments__status='completed'))
                    ).values('paid')[:1]
                )
            ).aggregate(
                total_due=Sum(
                    F('final_total_cost') - Coalesce('amount_paid', 0),
                    output_field=DecimalField()
                )
            )['total_due'] or Decimal('0.0')
    )

    return {
        'total_purchase': total_purchase,
        'purchase_including_tax': total_purchase + total_tax,
        'purchase_tax': total_tax,
        'total_purchase_return': Decimal('0.0'),  # Placeholder for future implementation
        'purchase_due': purchase_due
    }


def calculate_sale_metrics(start_date, end_date, location=None):
    """
    Calculate sale metrics for given date range and location.
    """
    from apps.ecom.models import Order, OrderLine

    # Base query for sales
    sale_query = Q(
        created_at__date__range=(start_date, end_date),
        status__in=['delivered', 'shipped']
    )

    # Add location filter if specified
    # if location:
    #     sale_query &= Q(shipping_address__city=location)

    # Calculate metrics
    sale_list = Order.objects.filter(sale_query)

    total_sale = sale_list.aggregate(
        total_sale=Sum('total_amount')
    )['total_sale'] or Decimal('0.0')

    total_sale_tax = sale_list.aggregate(
        total_tax=Sum(F('total_amount') * 0.15, output_field=DecimalField())
    )['total_tax'] or Decimal('0.0')

    total_sale_return = Decimal('0.0')  # Placeholder for future implementation

    sale_due = sale_list.filter(payment_status='not_paid').aggregate(
        total_due=Sum('total_amount')
    )['total_due'] or Decimal('0.0')

    return {
        'total_sale': total_sale,
        'sale_including_tax': total_sale + total_sale_tax,
        'total_sale_return': total_sale_return,
        'sale_due': sale_due
    }


class PurchaseSaleReportView(LoginRequiredMixin, TemplateView):
    """
    View for displaying purchase and sale report with custom date range support.
    """
    template_name = 'reports/purchase_sale_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filters from request
        date_filter = self.request.GET.get('date_filter', 'current_financial_year')
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        location = self.request.GET.get('location')

        # Get date range based on filter
        start_date, end_date = get_date_range(date_filter, start_date_str, end_date_str)

        # Calculate metrics
        purchase_metrics = calculate_purchase_metrics(start_date, end_date, location)
        sale_metrics = calculate_sale_metrics(start_date, end_date, location)

        # Calculate overall metrics
        overall = {
            'sale_minus_purchase': (sale_metrics['total_sale'] - sale_metrics['total_sale_return']) - (
                        purchase_metrics['total_purchase'] - purchase_metrics['total_purchase_return']),
            'due_amount': (sale_metrics['sale_due'] - purchase_metrics['purchase_due'])
        }

        # Update context
        context.update({
            'purchase_metrics': purchase_metrics,
            'sale_metrics': sale_metrics,
            'overall': overall,
            'start_date': start_date,
            'end_date': end_date,
            'selected_location': location,
            'date_filter': date_filter,
            'custom_start_date': start_date_str,
            'custom_end_date': end_date_str,
            'locations': self.get_locations()  # Add this method based on your location model
        })

        return context

    def get_locations(self):
        """
        Get list of available locations.
        Implement this based on your location model.
        """
        # Example implementation:
        # return Location.objects.filter(is_active=True)
        return []
