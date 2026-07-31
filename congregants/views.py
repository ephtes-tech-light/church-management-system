
from rest_framework import viewsets
from rest_framework.views import APIView, Response
from congregants.models import Donation, Event, Family, Member, Ministry
from congregants.serializers import DonationSerializer, EventSerializer, FamilySerializer, MemberSerializer, MinitstrySerializer


from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
# Create your views here.
class FamilyViewSet(viewsets.ModelViewSet):
    queryset=Family.objects.all().order_by('name')
    serializer_class=FamilySerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset=Member.objects.all().order_by('first_name','last_name')
    serializer_class=MemberSerializer
    filterset_fields = ['membership_status', 'family']

    def get_queryset(self):
        queryset = self.queryset
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        return queryset
class MinistryViewSet(viewsets.ModelViewSet):
    queryset=Ministry.objects.all().order_by('name')
    serializer_class=MinitstrySerializer 
class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all().order_by('start_time')
    serializer_class=EventSerializer
    def get_queryset(self):
        queryset = self.queryset
        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming == 'true':
            queryset = queryset.filter(start_time__gte=timezone.now())
        return queryset


class DonationViewSet(viewsets.ModelViewSet):
    queryset=Donation.objects.all().order_by('-date','-created_at')
    serializer_class=DonationSerializer
class DashboardStatsView(APIView):
     def get(self, request):
        now = timezone.now()
        thirty_days_ago = now.date() - timedelta(days=30)

        # Basic Stats
        total_members = Member.objects.count()
        active_members = Member.objects.filter(membership_status='active').count()
        total_ministries = Ministry.objects.count()
        
        # Financial Stats
        total_donated = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0.00
        donations_last_30_days = Donation.objects.filter(date__gte=thirty_days_ago).aggregate(total=Sum('amount'))['total'] or 0.00

        # Recent Donations (last 5)
        recent_donations = Donation.objects.all().order_by('-date', '-created_at')[:5]
        recent_donations_serialized = DonationSerializer(recent_donations, many=True).data

        # Upcoming Events (next 4)
        upcoming_events = Event.objects.filter(end_time__gte=now).order_by('start_time')[:4]
        upcoming_events_serialized = EventSerializer(upcoming_events, many=True).data

        # Donation Breakdown by Purpose
        purpose_breakdown = Donation.objects.values('purpose').annotate(total=Sum('amount')).order_by('-total')
        purpose_data = {item['purpose']: float(item['total']) for item in purpose_breakdown}
        # Fill missing default purposes
        all_purposes = ['tithe', 'offering', 'building_fund', 'missions', 'other']
        for p in all_purposes:
            if p not in purpose_data:
                purpose_data[p] = 0.0

        # Donation History (last 6 months)
        six_months_ago = now.date() - timedelta(days=180)
        history = (
            Donation.objects.filter(date__gte=six_months_ago)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        
        history_data = []
        for h in history:
            if h['month']:
                history_data.append({
                    'month': h['month'].strftime('%B %Y'),
                    'amount': float(h['total'])
                })

        return Response({
            'total_members': total_members,
            'active_members': active_members,
            'total_ministries': total_ministries,
            'total_donated': float(total_donated),
            'donations_last_30_days': float(donations_last_30_days),
            'recent_donations': recent_donations_serialized,
            'upcoming_events': upcoming_events_serialized,
            'purpose_breakdown': purpose_data,
            'giving_history': history_data
        })
