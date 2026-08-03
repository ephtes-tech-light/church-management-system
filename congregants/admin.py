from django.contrib import admin

from congregants.models import Donation, Event, Family, Member, Ministry

admin.site.site_header = "MKC Church Management System"
admin.site.site_title = "MKC Church Admin Portal"
admin.site.index_title = "Welcome to the Church Administration Center"
#inlines

class MemberInline(admin.TabularInline):
    model=Member
    fields=('first_name','last_name','family_relationship','membership_status','phone')
    extra=1
    show_change_link=True
    

class DonationInline(admin.TabularInline):
    model=Donation
    fields=('date', 'amount', 'purpose', 'payment_method')
    extra=0
    readonly_fields= ('created_at',)
    show_change_link = True

# Register your models here.
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count','created_at')
    search_fields=('name',)
    inlines = [MemberInline]
    readonly_fields= ('created_at',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description='Members Count'

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'email', 'phone', 'membership_status', 'join_date', 'family')
    list_filter=('membership_status', 'gender', 'join_date', 'family')
    search_fields=('first_name', 'last_name', 'email', 'phone','family__name')
    ordering=('first_name', 'last_name')
    list_editable = ('membership_status',)
    inlines = [DonationInline]
    autocomplete_fields = ('family',)
    list_per_page=25
    readonly_fields = ('created_at',)

    # Grouping form fields logically in the edit view
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), ('gender', 'date_of_birth'), 'photo_url')
        }),
        ('Contact Information', {
            'fields': (('email', 'phone'), 'address')
        }),
        ('Church Membership', {
            'fields': ('membership_status', 'join_date', ('family', 'family_relationship'))
        }),
      
    )

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display=('name', 'leader', 'member_count', 'created_at')
    search_fields=('name', 'description')

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = "Member Count"

    search_fields = ('name', 'description', 'leader__first_name', 'leader__last_name')
    filter_horizontal = ('members',)  # Dual-box selector for ManyToMany relations
    autocomplete_fields = ('leader',)
    



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

