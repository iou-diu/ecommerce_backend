from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.ecom.serializers import SupportTicketSerializer, SupportTicketMessageSerializer
from apps.ecom.models import SupportTicket, SupportTicketMessage
from django.contrib.auth import get_user_model

class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'ticket_id'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SupportTicket.objects.all()
        elif user.is_staff:
            return SupportTicket.objects.filter(assigned_to=user)
        return SupportTicket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def assign(self, request, ticket_id=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can assign tickets"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        ticket = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if assigned_to_id:
            User = get_user_model()
            assigned_to = get_object_or_404(User, id=assigned_to_id)
            ticket.assigned_to = assigned_to
        else:
            ticket.assigned_to = request.user
            
        ticket.status = 'in_progress'
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def close(self, request, ticket_id=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can close tickets"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.is_closed = True
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_message(self, request, ticket_id=None):
      ticket = self.get_object()  # Get the specific ticket instance based on ticket_id
      serializer = SupportTicketMessageSerializer(data=request.data)
    
      if serializer.is_valid():
            serializer.save(
            ticket=ticket,  # Automatically associate the message with the ticket
            sender=request.user  # Set the sender to the current user
             )
            # Re-fetch the ticket to get updated messages
            ticket_serializer = self.get_serializer(ticket)
            return Response(ticket_serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
