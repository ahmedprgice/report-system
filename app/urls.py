from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('visitor/', views.visitor_view, name='visitor'),
    path('visitor_dashboard/', views.visitor_dashboard, name='visitor_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),  # Ensure this points to the correct view
    path('security/dashboard/', views.security_dashboard, name='security_dashboard'),
    path('security/login/', views.security_login, name='security_login'),
    path('dashboard/create_report/', views.create_report, name='create_report'),
    path('visitor_dashboard/create_report/', views.create_report, name='create_report'),
    path('dashboard/update_profile/', views.update_profile, name='update_profile'),
    path('get_report/<uuid:report_id>/', views.get_report, name='get_report'),
    path('share_location/<uuid:id>/', views.share_location, name='share_location'),
    path('track_visitor/<uuid:visitor_id>/', views.track_visitor, name='track_visitor'),
    path('check_transactions/<uuid:visitor_id>/', views.check_transactions, name='check_transactions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
