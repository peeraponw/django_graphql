from atexit import register
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

# # # Query
class Query(graphene.ObjectType):
    pass



# # # Mutation
class Mutation(graphene.ObjectType):
    pass
    
