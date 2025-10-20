"""
URL configuration for ecommerce_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.user.views import HomeView, PaymentHandlerView
from api.urls import api_related_urlpatterns

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('payment-verify/', PaymentHandlerView.as_view(), name='payment-success'),
    path("admin/", admin.site.urls),
    path("accounting/", include("apps.accounting.urls")),
    path("ecommerce/", include("apps.ecom.urls")),
    path("solutions/", include("apps.solutions.urls")),
    path("inventory/", include("apps.inventory.urls")),
    # path('accounts/', include('allauth.urls')),
    path("account/", include("apps.user.urls")),
    path("select2/", include("django_select2.urls")),
    path("aiapps/", include("apps.aiapps.urls")),
    path("promo/", include("apps.promo.urls")),
    path("cms/", include("apps.cms.urls")),
    path("reports/", include("apps.report.urls")),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += [
    path('api/v1/', include((api_related_urlpatterns, 'api'), namespace='v1'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Ecommerce"
admin.site.index_title = "Admin area"
admin.site.site_title = "DCL"
