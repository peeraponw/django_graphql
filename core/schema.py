import graphene
import graphql_jwt

import timeclock.schema
import users.schema

class Query(users.schema.Query, timeclock.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, timeclock.schema.Mutation, graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)