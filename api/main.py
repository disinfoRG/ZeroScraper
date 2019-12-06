from flask import Flask
from flask_graphql import GraphQLView
import graphene
import pugsql
import os

queries = pugsql.module("queries/")

queries.connect(os.getenv("DB_URL"))


class ArticleHistory(graphene.ObjectType):
    count = graphene.Int()

    def resolve_count(parent, info):
        return 0


class ArticlesResult(graphene.ObjectType):
    count = graphene.Int()
    hist = graphene.List(ArticleHistory)

    def resolve_count(parent, info):
        return parent["count"]

    def resolve_hist(parent, info):
        return []


class Site(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    url = graphene.String()
    type = graphene.String()
    is_active = graphene.Boolean()
    articles = graphene.Field(ArticlesResult)

    def resolve_id(parent, info):
        return parent["site_id"]

    def resolve_name(parent, info):
        return parent["name"]

    def resolve_url(parent, info):
        return parent["url"]

    def resolve_type(parent, info):
        return parent["type"]

    def resolve_is_active(parent, info):
        if parent["is_active"] is None or parent["is_active"] == 0:
            return False
        return True

    def resolve_articles(parent, info):
        return queries.get_site_articles(site_id=parent["site_id"])


class SitesResult(graphene.ObjectType):
    count = graphene.Int()
    items = graphene.List(Site)

    def resolve_count(parent, info):
        print(queries.get_sites_count())
        return queries.get_sites_count()["count"]

    def resolve_items(parent, info):
        if parent["site_id"] is None:
            return queries.get_sites()
        else:
            return [queries.get_site(id=parent["site_id"])]


class Query(graphene.ObjectType):
    sites = graphene.Field(SitesResult)

    def resolve_sites(parent, info, id=None):
        return {"site_id": id}


schema = graphene.Schema(query=Query)


app = Flask(__name__)
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run()
