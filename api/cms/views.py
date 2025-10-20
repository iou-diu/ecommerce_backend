from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from apps.cms.models import HomeSlider, Gallery, Brochure, NewsPress, ContactForm
from apps.solutions.models import Solution
from .serializers import HomeSliderSerializer, GallerySerializer, BrochureSerializer, NewsPressSerializer, \
    NewsPressListSerializer, SolutionDetailSerializer, SolutionListSerializer, ContactFormSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class HomeSliderViewSet(viewsets.ModelViewSet):
    queryset = HomeSlider.objects.all()
    serializer_class = HomeSliderSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
            if not self.request.user.is_staff:
                self.permission_denied(self.request, message="Only staff can add, edit, or delete.")
        return [permission() for permission in permission_classes]


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['type', 'is_featured']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
            if not self.request.user.is_staff:
                self.permission_denied(self.request, message="Only staff can add, edit, or delete.")
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        total_items = queryset.count()
        total_photo = queryset.filter(type='photo').count()
        total_video = queryset.filter(type='video').count()
        total_audio = queryset.filter(type='audio').count()
        response.data = {
            'count': total_items,
            'total_photo': total_photo,
            'total_video': total_video,
            'total_audio': total_audio,
            'next': response.data.get('next'),
            'previous': response.data.get('previous'),
            'results': response.data.get('results', response.data)
        }
        return response


class BrochureViewSet(viewsets.ModelViewSet):
    """
    This viewset will be used to manage brochures.
    """
    # Assuming you have a Brochure model and serializer
    queryset = Brochure.objects.all()
    serializer_class = BrochureSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
            if not self.request.user.is_staff:
                self.permission_denied(self.request, message="Only staff can add, edit, or delete.")
        return [permission() for permission in permission_classes]


class NewsPressViewSet(viewsets.ModelViewSet):
    """
    This viewset will be used to manage news and press releases.
    """
    # Assuming you have a NewsPress model and serializer
    queryset = NewsPress.objects.all()
    serializer_class = NewsPressSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['status', 'is_featured']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsPressListSerializer
        return NewsPressSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
            if not self.request.user.is_staff:
                self.permission_denied(self.request, message="Only staff can add, edit, or delete.")
        return [permission() for permission in permission_classes]


class PublicSolutionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Solution.objects.all().order_by('-created_at')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['categories']
    search_fields = ['title', 'short_description']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SolutionDetailSerializer
        return SolutionListSerializer


from rest_framework import mixins

class ContactFormViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = ContactForm.objects.all().order_by('-created_at')
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # Public API
