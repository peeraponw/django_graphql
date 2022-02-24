from atexit import register
import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from .models import Clock, ClockedHours
from datetime import datetime

class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        fields = ("id", "user", "clocked_in", "clocked_out")
        
class ClockedHoursType(DjangoObjectType):
    class Meta:
        model = ClockedHours
        fields = ("today", "current_week", "current_month")

class ClockInMutation(graphene.Mutation):
    clock = graphene.Field(ClockType)
    
    @classmethod
    def mutate(cls, root, info):
        utctime = datetime.utcnow()
        clock = Clock(clocked_in=utctime)
        clock.save()
        return ClockInMutation(clock=clock)
        
class ClockOutMutation(graphene.Mutation):
    clock = graphene.Field(ClockType)
    
    @classmethod
    def mutate(cls, root, info):
        pass
    
class ClocedHoursType(DjangoObjectType):
    class Meta:
        model = ClockedHours
        fields = ("today", "current_week", "current_month")
    

class AuthMutation(graphene.ObjectType):
    create_user = mutations.Register.Field()
    obtain_token = mutations.ObtainJSONWebToken.Field()
    clock_in = ClockInMutation.Field()
    clock_out = ClockOutMutation.Field()

class Query(graphene.ObjectType):
    pass
class Mutation(graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)