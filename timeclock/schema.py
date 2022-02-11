from atexit import register
import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    create_user = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    obtain_token = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    # clock_in = 
    # clock_out = 

class Query(UserQuery, MeQuery, graphene.ObjectType):
    
    
    # current_clock = 
    # clocked_hours = 
    # today = 
    # curent_week = 
    # current_month = 
    pass
class Mutation(AuthMutation, graphene.ObjectType):
    pass
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)