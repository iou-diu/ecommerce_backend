from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.paginator import Paginator

from apps.cms.models import HomeSlider, ContactForm


# Create your views here.
class HomeSliderView(ListView):
    model = HomeSlider  # Assuming HomeSlider is imported or defined elsewhere
    template_name = 'cms/slider.html'


class ContactFormListView(ListView):
    model = ContactForm
    template_name = 'contacts-data.html'
    context_object_name = 'contacts'
    paginate_by = 20


def contact_form_ajax(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = ContactForm.objects.all()
    if search_value:
        queryset = queryset.filter(
            name__icontains=search_value
        )

    total = queryset.count()
    paginator = Paginator(queryset, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = []
    for contact in page.object_list:
        data.append([
            contact.name,
            contact.email,
            contact.phone,
            contact.subject,
            contact.message,
            contact.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    })
