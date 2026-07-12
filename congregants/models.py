from datetime import timezone

from django.db import models

class Family(models.Model):
    name=models.CharField(max_length=100)
    notes=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbouse_name_plural="Families"

    def __str__(self):
        return self.name

class Member(models.Model):
    MEMBER_STATUS=[('active','Active Member'),
                   ('guest','Guest'),
                   ('inactive','Inactive'),]
    GENDER=[('M','Male'),
            ('F','Female'),]
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20)
    membership_status=models.CharField(max_length=10,choices=MEMBER_STATUS)
    address=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=1,choices=GENDER)
    join_date=models.DateField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    family=models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    family_relationship=models.CharField(max_length=50, blank=True, null=True, help_text="Husband, Wife, Son, Daughter")
    photo_url=models.URLField(max_length=500, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Ministry(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True)
    leader=models.ForeignKey(Member,related_name='led_ministries',blank=True)
    members=models.ManyToManyField(Member,related_name="ministries")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbouse_name_plural="Ministries"
    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = [
        ('service','Sunday Service'),
        ('prayer','Prayer Meeting'),
        ('youth','Youth Group'),
        ('other', 'Other Event')
    ]
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    location=models.CharField(max_length=100,blank=True,null=True)
    event_type=models.CharField(max_length=20, choices=EVENT_TYPES)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Dontaion(models.Model):
    PURPOSE_CHOICE=[
        ('tithe',"Thite"),
        ('offering',"Offering"),
        ('missions',"Missions"),
        ('other',"Other"),
    ]
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online'),
    ]
    member=models.ForeignKey(Member,on_delete=models.SET_NULL, null=True, blank=True, related_name='donations', help_text="keep blank for anonymous donations")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField(default=timezone.now)
    purpose=models.CharField(max_length=20, choices=PURPOSE_CHOICE, default='tithe')
    payment_method=models.CharField(max_length=20, choices=METHOD_CHOICES,default='cash')
    notes=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        source=f"{self.member}"if self.member else "Anonymous"
        return f"{source} - ${self.amount} ({self.get_purpose_display()}) on {self.date}"







