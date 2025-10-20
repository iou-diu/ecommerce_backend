from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django_tables2 import SingleTableView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import SupportTicket, SupportTicketMessage
from .forms import SupportTicketForm, SupportTicketMessageForm
from .tables import SupportTicketTable

def is_staff(user):
    return user.is_staff

class SupportTicketListView(SingleTableView):
    model = SupportTicket
    table_class = SupportTicketTable
    template_name = "support_ticket_list.html"
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_superuser:  # Staff user sees tickets assigned to them
            print("True")
            return SupportTicket.objects.all()
        elif user.is_staff:  # Admin user sees all tickets
            # print(SupportTicket.objects.all())
            return SupportTicket.objects.filter(assigned_to=user)
        else:  # General user sees only their created tickets
            return SupportTicket.objects.filter(user=user)
# class SupportTicketDetailView(View):
#     template_name = 'support_ticket_detail.html'

#     def get(self, request, ticket_id, *args, **kwargs):
#         ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
#         messages = SupportTicketMessage.objects.filter(ticket=ticket).order_by('created_at')
#         message_form = SupportTicketMessageForm()
#         return render(request, self.template_name, {
#             'ticket': ticket,
#             'messages': messages,
#             'message_form': message_form
#         })

#     def post(self, request, ticket_id, *args, **kwargs):
#         ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
#         message_form = SupportTicketMessageForm(request.POST)
#         if message_form.is_valid():
#             message = message_form.save(commit=False)
#             message.ticket = ticket
#             message.user = request.user
#             message.save()
#             return redirect('ticket_detail', ticket_id=ticket.ticket_id)
#         messages = SupportTicketMessage.objects.filter(ticket=ticket).order_by('created_at')
#         return render(request, self.template_name, {
#             'ticket': ticket,
#             'messages': messages,
#             'message_form': message_form
#         })
from django.contrib import messages as django_messages

class SupportTicketDetailView(View):
    template_name = 'support_ticket_detail.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        messages = SupportTicketMessage.objects.filter(ticket=ticket).order_by('created_at')
        message_form = SupportTicketMessageForm()
        print("Messages",messages)
        print("Messages Form",message_form)
        # Get all users for the dropdown if the user is staff or superuser
        user_list = get_user_model().objects.filter(is_active=True) if request.user.is_staff or request.user.is_superuser else None

        return render(request, self.template_name, {
            'ticket': ticket,
            'messages': messages,
            'message_form': message_form,
            'user_list': user_list,
        })

    def post(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        message_form = SupportTicketMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.save()
            django_messages.success(request, "Message sent successfully.")
            return redirect('ticket_detail', ticket_id=ticket.ticket_id)
        messages = SupportTicketMessage.objects.filter(ticket=ticket).order_by('created_at')
        return render(request, self.template_name, {
            'ticket': ticket,
            'messages': messages,
            'message_form': message_form
        })
    
from django.contrib.auth import get_user_model

@method_decorator([login_required, user_passes_test(is_staff)], name='dispatch')
class SupportTicketAssignView(View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        
        # Get the selected user from POST data
        selected_user_id = request.POST.get('assigned_to')
        
        # Assign to the selected user if provided, otherwise assign to the current user
        if selected_user_id:
            selected_user = get_object_or_404(get_user_model(), id=selected_user_id)
            ticket.assigned_to = selected_user
        else:
            ticket.assigned_to = request.user
            
        ticket.status = 'in_progress'
        ticket.save()
        
        return redirect('ticket_detail', ticket_id=ticket.ticket_id)

@method_decorator([login_required, user_passes_test(is_staff)], name='dispatch')
class SupportTicketCloseView(View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        ticket.status = 'closed'
        ticket.save()
        return redirect('ticket_detail', ticket_id=ticket.ticket_id)

class SupportTicketCreateView(LoginRequiredMixin, View):
    template_name = 'support_ticket_create.html'
    success_url = reverse_lazy('support_ticket_list')

    def get(self, request, *args, **kwargs):
        form = SupportTicketForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
