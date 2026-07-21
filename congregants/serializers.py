from rest_framework import serializers

from congregants.models import Donation, Event, Family, Member, Ministry

class FamilySerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(source='members.count',read_only=True)
    class Meta:
        model=Family
        fields=['id','name','notes','member_count','created_at']

class MemberSerializer(serializers.ModelSerializer):
    family_name=serializers.CharField(source='family.name',read_only=True)
    full_name=serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields=[
           'id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 
            'address', 'date_of_birth', 'gender', 'membership_status', 
            'join_date', 'family', 'family_name', 'family_relationship', 
            'photo_url', 'created_at'
          ]  
        def get_full_name(self, obj):
            return f"{obj.first_name} {obj.last_name}"

class MinitstrySerializer(serializers.ModelSerializer):
    leader_name=serializers.SerializerMethodField()
    member_count = serializers.IntegerField(source='members.count', read_only=True)
    
    class Meta:
        model = Ministry
        fields=['id', 'name', 'description', 'leader', 'leader_name', 'members', 'member_count', 'created_at']

        def get_leader_name(self,obj):
            if obj.leader:
               return f"{obj.leader.first_name} {obj.leader.last_name}" 
            return "No Leader"

class EventSerializer(serializers.ModelSerializer):
    event_type_display=serializers.CharField(source='get_event_type_display',read_only=True)

    class Meta:
        model = Event
        fields= ['id', 'title', 'description', 'start_time', 'end_time', 'location', 'event_type', 'event_type_display', 'created_at']

class DonationSerializer(serializers.ModelSerializer):
    member_name=serializers.SerializerMethodField()
    purpose_display = serializers.CharField('get_payment_method_display', read_only=True)
    class Meta:
        model=Donation
        fields = [
            'id', 'member', 'member_name', 'amount', 'date', 'purpose', 
            'purpose_display', 'payment_method', 'payment_method_display', 
            'notes', 'created_at'
        ]
    def get_member_name(self,obj):
        if obj.member:
            return f"{obj.member.first_name} {obj.member.last_name}"
        return "Anonymous"