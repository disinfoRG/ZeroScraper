from flask import Flask
from flask_graphql import GraphQLView
import graphene
import pugsql
import os

queries = pugsql.module("queries/")

queries.connect(os.getenv("DB_URL"))


class Site(graphene.ObjectType):
    name = graphene.String()
    url = graphene.String()
    articles_count = graphene.Int()

    def resolve_name(parent, info):
        return parent["name"]

    def result_url(parent, info):
        return parent["url"]

    def resolve_articles_count(parent, info):
        return parent["articles_count"]


class Query(graphene.ObjectType):
    sites = graphene.List(Site)
    sites_count = graphene.Int()

    def resolve_sites(parent, info):
        return queries.get_sites_info()

    def resolve_sites_count(parent, info):
        return queries.get_sites_count()["sites_count"]


schema = graphene.Schema(query=Query)


app = Flask(__name__)
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run()
