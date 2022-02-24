import graphene
from graphene_django import DjangoObjectType
from .models import Clock, ClockedHours


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
    clock = graphene.Field(ClockType)
    
    def mutate(self, info, **kwargs):
        pass

class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType)
    
    def mutate(self, info, **kwargs):
        pass