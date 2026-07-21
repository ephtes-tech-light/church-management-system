from django.contrib import admin

from congregants.models import Donation, Event, Family, Member, Ministry

# Register your models here.
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count','created_at')
    search_fields=('name',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description='Members Count'

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'email', 'phone', 'membership_status', 'join_date', 'family')
    list_filter=('membership_status', 'gender', 'join_date', 'family')
    search_fields=('first_name', 'last_name', 'email', 'phone')
    ordering=('first_name', 'last_name')

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display=('name', 'leader', 'member_count', 'created_at')
    search_fields=('name', 'description')

    def member_count(self, obj):
        return obj.member_count()
    member_count.short_description = "Member Count"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','event_type','start_time','end_time','location')
    list_filter = ('event_type','start_time','end_time', 'location')
    search_fields = ('title','description','location')
    ordering = ('start_time',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount','date', 'purpose', 'payment_method')
    list_filter = ('purpose', 'payment_method', 'date')
    search_fields = ('member_first_name', 'member_last_name','notes')
    ordering = ('-date', 'created_at')
    