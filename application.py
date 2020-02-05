from flask import Flask, request
from flask_restful import Resource, Api
from newsSpiders.webapi import sites, articles
import pugsql
import os
from dotenv import load_dotenv

load_dotenv()
queries = pugsql.module("queries")
queries.connect(os.getenv("DB_URL"))

app = Flask(__name__)
api = Api(app)


class FindArticleByID(Resource):
    def get(self, article_id):
        result = articles.get_article_by_id(queries, article_id)
        return result


class FindArticleByURL(Resource):
    def get(self):
        url = request.args.get("url")
        result = articles.get_article_by_url(queries, url)
        if "error_message" in result.keys():
            return result, 404
        return result


class SiteArticleCount(Resource):
    def get(self, site_id):
        article_count = sites.get_article_count(queries, site_id)
        return article_count


class SiteLatestArticle(Resource):
    def get(self, site_id):
        latest_article = sites.get_latest_article(queries, site_id)
        return latest_article


class SitesWarning(Resource):
    def get(self, site_id):
        warning_msg = f"Are you looking for </sites/{site_id}/article_count> or </sites/{site_id}/latest_article>?"
        return {"message": warning_msg}, 404


class Hello(Resource):
    def get(self):
        welcome_msg = "Hello, welcome to the api of g0v 0archive"
        return {"message": welcome_msg}


api.add_resource(FindArticleByID, "/articles/<int:article_id>")
api.add_resource(FindArticleByURL, "/articles")
api.add_resource(SitesWarning, "/sites/<int:site_id>", "/sites/<int:site_id>/")
api.add_resource(SiteArticleCount, "/sites/<int:site_id>/article_count")
api.add_resource(SiteLatestArticle, "/sites/<int:site_id>/latest_article")
api.add_resource(Hello, "/")

if __name__ == "__main__":
    app.run(debug=True)
