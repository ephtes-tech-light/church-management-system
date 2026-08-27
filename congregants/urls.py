from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (FamilyViewSet, MemberViewSet, MinistryViewSet, 
EventViewSet, DonationViewSet, DashboardStatsView)

router = DefaultRouter()
router.register(r'families', FamilyViewSet, basename='family')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'events', EventViewSet, basename='event')
router.register(r'donations', DonationViewSet, basename='donation')


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]