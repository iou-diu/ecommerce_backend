# views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from api.business_setting.serializers import BusinessSettingSerializer
from apps.ecom.models import BusinessSetting
from apps.user.permission import IsAdminOrStaff


class BusinessSettingViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = BusinessSetting.objects.all()
    serializer_class = BusinessSettingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['key', ]
    http_method_names = ['get', ]
