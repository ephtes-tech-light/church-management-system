"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
#from rest_framework import DefaultRouter
from rest_framework.routers import DefaultRouter  # ✅ Correct import

from congregants.views import DashboardStatsView, DonationViewSet, EventViewSet, FamilyViewSet, MemberViewSet, MinistryViewSet

router=DefaultRouter()
router.register(r'families',FamilyViewSet, basename='family')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'events', EventViewSet, basename='event')
router.register(r'donations', DonationViewSet, basename='donation')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('dashboard-stats/', DashboardStatsView.as_view())
]


