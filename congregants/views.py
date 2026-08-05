
from rest_framework import viewsets, filters
from rest_framework.views import APIView, Response
from congregants.models import Donation, Event, Family, Member, Ministry
from congregants.serializers import DonationSerializer, EventSerializer, FamilySerializer, MemberSerializer, MinitstrySerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
# Create your views here.
class FamilyViewSet(viewsets.ModelViewSet):

    # prefetch_related reduces queries when fetching family members
    queryset=Family.objects.prefetch_related('members').order_by('name')
    serializer_class=FamilySerializer
    search_fields=['name']

class MemberViewSet(viewsets.ModelViewSet):
  
    queryset=Member.objects.select_related('family')
    serializer_class=MemberSerializer
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['membership_status', 'family']
    search_fields=['first_name','last_name','email','phone']
    ordering_fields=['name']
    
class MinistryViewSet(viewsets.ModelViewSet):
    
    queryset=Ministry.objects.select_related('leader').prefetch_related('members')
    serializer_class=MinitstrySerializer 
    filter_backends=[filters.SearchFilter]
    search_fields=['name']
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
     from datetime import timedelta
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class DashboardStatsView(APIView):
    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now.date() - timedelta(days=30)
        six_months_ago = now.date() - timedelta(days=180)

        # 1. Combined Member Stats (1 Query)
        member_stats = Member.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(membership_status='active'))
        )

        # 2. Combined Financial Totals (1 Query)
        donation_stats = Donation.objects.aggregate(
            total=Sum('amount'),
            last_30=Sum('amount', filter=Q(date__gte=thirty_days_ago))
        )

        # 3. Quick Count
        total_ministries = Ministry.objects.count()

        # 4. Recent Donations with JOIN (1 Query)
        recent_donations = (
            Donation.objects.select_related('member')
            .order_by('-date', '-created_at')[:5]
        )
        recent_donations_serialized = DonationSerializer(recent_donations, many=True).data

        # 5. Upcoming Events with Field Optimization (1 Query)
        upcoming_events = (
            Event.objects.filter(end_time__gte=now)
            .only('id', 'title', 'start_time', 'end_time')
            .order_by('start_time')[:4]
        )
        upcoming_events_serialized = EventSerializer(upcoming_events, many=True).data

        # 6. Donation Breakdown by Purpose (1 Query)
        purpose_breakdown = (
            Donation.objects.values('purpose')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        purpose_data = {
            p: 0.0 for p in ['tithe', 'offering', 'building_fund', 'missions', 'other']
        }
        for item in purpose_breakdown:
            if item['purpose'] in purpose_data:
                purpose_data[item['purpose']] = float(item['total'])

        # 7. 6-Month Giving History (1 Query)
        history = (
            Donation.objects.filter(date__gte=six_months_ago)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        history_data = [
            {
                'month': h['month'].strftime('%B %Y'),
                'amount': float(h['total'])
            }
            for h in history if h['month']
        ]

        return Response({
            'total_members': member_stats['total'],
            'active_members': member_stats['active'],
            'total_ministries': total_ministries,
            'total_donated': float(donation_stats['total'] or 0.00),
            'donations_last_30_days': float(donation_stats['last_30'] or 0.00),
            'recent_donations': recent_donations_serialized,
            'upcoming_events': upcoming_events_serialized,
            'purpose_breakdown': purpose_data,
            'giving_history': history_data
        })
