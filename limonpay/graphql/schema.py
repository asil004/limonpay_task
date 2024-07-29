import graphene

from limonpay.graphql.mutation import Mutation
from limonpay.graphql.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
