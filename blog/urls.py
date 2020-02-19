from django.conf.urls import url
from django.urls import path
from .views import index, index_details, user_login

from django.contrib.auth import views as auth_views
from . import views
from django.http import request
# app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('login', user_login, name='login'),
    path('details/<slug:slug>/', index_details, name='detail'),
    # url(r'^$', views.dashboard, name='dashboard'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    # login/logout urls
    url(r'^log-out/$', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^logout-then-login/$', auth_views.logout_then_login(request,login_url='login'), name='logout_then_login'),
    # change password urls
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),
    url(r'^password-change/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change'),
    # resrore password urls
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_confirm')

]
