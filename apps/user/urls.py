from django.urls import path, re_path, include
from allauth.account import views as auth_views
from allauth import app_settings
from .views import (StaffUserCreateView, StaffUserDeleteView, StaffUserListView, StaffUserUpdateView, CustomerUserCreateView, CustomerUserDeleteView, CustomerUserListView, CustomerUserUpdateView)

from importlib import import_module
from . import views

urlpatterns = [
    path('customeruser/<int:pk>/delete/', CustomerUserDeleteView.as_view(), name='customeruser_delete'),
    path('customeruser/<int:pk>/update/', CustomerUserUpdateView.as_view(), name='customeruser_update'),
    path('customeruser/add/', CustomerUserCreateView.as_view(), name='customeruser_add'),
    path('customeruser/', CustomerUserListView.as_view(), name='customeruser_list'),
    path('staffuser/<int:pk>/delete/', StaffUserDeleteView.as_view(), name='staffuser_delete'),
    path('staffuser/<int:pk>/update/', StaffUserUpdateView.as_view(), name='staffuser_update'),
    path('staffuser/add/', StaffUserCreateView.as_view(), name='staffuser_add'),
    path('staffuser/', StaffUserListView.as_view(), name='staffuser_list'),


    # path("signup/", auth_views.signup, name="account_signup"),
    path("signup/", auth_views.login, name="account_signup"),
    path("login/", auth_views.login, name="account_login"),
    path("logout/", auth_views.logout, name="account_logout"),
    path("password/change/", auth_views.password_change, name="account_change_password"),
    path("password/set/", auth_views.password_set, name="account_set_password"),
    # path("inactive/", auth_views.account_inactive, name="account_inactive"),
    path("email/", auth_views.email, name="account_email"),
    path("confirm-email/", auth_views.email_verification_sent, name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", auth_views.confirm_email, name="account_confirm_email"),
    path("password/reset/", auth_views.password_reset, name="account_reset_password"),
    path("password/reset/done/", auth_views.password_reset_done, name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", auth_views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", auth_views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),

    path('group-permissions/', views.group_permission_view, name='group_permission_view'),
   
]

if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]


