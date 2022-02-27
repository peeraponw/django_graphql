import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum

from users.schema import UserType
from users.schema import CreateUser

from timeclock.models import Clock, ClockedHours
from timeclock.schema import ClockType, ClockedHoursType
from timeclock.schema import ClockIn, ClockOut


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    clocks = graphene.List(ClockType)
    my_clocks = graphene.List(ClockType)
    
    current_clock = graphene.Field(ClockType)
    clocked_hours = graphene.Field(ClockedHoursType)
    
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()
    
    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in")
        return user
    
    def resolve_clocks(self, info, **kwargs):
        return Clock.objects.all()
    
    def resolve_my_clocks(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in")
        return Clock.objects.filter(user=user)
    
    def resolve_current_clock(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in")
        return Clock.objects.filter(user=user, clocked_out=None).first()
        
    
    def resolve_clocked_hours(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in")
        now = timezone.now()
        this_year, this_week, today = now.isocalendar() # this follows ISO 8601 calendar but not Gregorian calendar
        # today part
        today_clock = Clock.objects.filter(user=user).filter(clocked_in__date__gte=now.date()).all()
        today_hours = 0
        for clock in today_clock:
            clockin = clock.clocked_in
            clockout = clock.clocked_out if clock.clocked_out else now
            hours = (clockout - clockin).seconds / 3600
            today_hours += hours
        # this week part
        this_week_clock = Clock.objects.filter(user=user).filter(clocked_in__week__gte=this_week).all()
        this_week_hours = 0
        for clock in this_week_clock:
            clockin = clock.clocked_in
            clockout = clock.clocked_out if clock.clocked_out else now
            hours = (clockout - clockin).seconds / 3600
            this_week_hours += hours
        # this month part
        this_month_clock = Clock.objects.filter(user=user).filter(clocked_in__month__gte=now.month).all()
        this_month_hours = 0
        for clock in this_month_clock:
            clockin = clock.clocked_in
            clockout = clock.clocked_out if clock.clocked_out else now
            hours = (clockout - clockin).seconds / 3600
            this_month_hours += hours
        c = ClockedHours.objects.create(today=today_hours, current_week=this_week_hours, current_month=this_month_hours)
        c.save()
        return c
        
        

class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field() # optional
    refresh_token = graphql_jwt.Refresh.Field() # optional
    create_user = CreateUser.Field()
    
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)