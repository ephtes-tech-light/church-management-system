from rest_framework import viewsets
from rest_framework.views import APIView
from congregants.models import Donation, Event, Family, Member, Ministry
from congregants.serializers import DonationSerializer, EventSerializer, FamilySerializer, MemberSerializer, MinitstrySerializer

# Create your views here.
class FamilyViewSet(viewsets.ModelViewSet):
    queryset=Family.objects.all().order_by('name')
    serializer_class=FamilySerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset=Member.objects.all().order_by('first_name','last_name')
    serializer_class=MemberSerializer

class MinistryViewSet(viewsets.ModelViewSet):
    queryset=Ministry.objects.all().order_by('name')
    serializer_class=MinitstrySerializer
class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all().order_by('start_time')
    serializer_class=EventSerializer
class DonationViewSet(viewsets.ModelViewSet):
    queryset=Donation.objects.all().order_by('-date','-created_at')
    serializer_class=DonationSerializer
#class DashboardStatsView(APIView):
