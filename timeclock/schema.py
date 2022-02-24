import graphene
from django.utils import timezone
from graphene_django import DjangoObjectType
from .models import Clock, ClockedHours
from users.schema import UserType

# # # Type
class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        # fields = ("id", "user", "clocked_in", "clocked_out")
        
class ClockedHoursType(DjangoObjectType):
    class Meta:
        model = ClockedHours
        # fields = ("today", "current_week", "current_month")
    
class ClockIn(graphene.Mutation):
    user = graphene.Field(UserType)
    clock = graphene.Field(ClockType)
    
    def mutate(self, info, **kwargs):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception("You must log in to start your clock")
        c = Clock.objects.create(user=user)
        return ClockIn(user=user, clock=c)
    
class ClockOut(graphene.Mutation):
    user = graphene.Field(UserType)
    clock = graphene.Field(ClockType)
    
    def mutate(self, info, **kwargs):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception("You must log in to end your clock")
        c = Clock.objects.filter(user=user, clocked_out=None).first()
        c.clocked_out = timezone.now()
        c.save()
        return ClockOut(user=user, clock=c)