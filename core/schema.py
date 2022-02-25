import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.schema import UserType
from users.schema import CreateUser

from timeclock.models import Clock
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
        pass

class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field() # optional
    refresh_token = graphql_jwt.Refresh.Field() # optional
    create_user = CreateUser.Field()
    
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)