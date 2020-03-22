from flask import Flask, request
from flask_restful import Resource, Api
import pugsql
import os
import time
from dotenv import load_dotenv
from newsSpiders.webapi import sites, articles, publications

app = Flask(__name__)
api = Api(app)

load_dotenv()
# scraper db
scraper_queries = pugsql.module("queries/")
scraper_queries.connect(os.getenv("DB_URL"))
# publication db
pub_queries = pugsql.module("queries/parser")
pub_queries.connect(os.getenv("PUB_DB_URL"))


class FindArticleByID(Resource):
    def get(self, article_id):
        result = articles.get_article_by_id(scraper_queries, article_id)
        return result


class FindArticleByURL(Resource):
    def get(self):
        url = request.args.get("url")
        result = articles.get_article_by_url(scraper_queries, url)
        print(result)
        if "error_message" in result[0].keys():
            return result, 404
        return result


class SiteArticleCount(Resource):
    def get(self, site_id):
        now = int(time.time())
        discover_from = request.args.get("discoverFrom", None)
        discover_until = request.args.get("discoverUntil", now)
        if discover_from:
            article_count = sites.get_article_count_in_interval(
                scraper_queries, site_id, int(discover_from), int(discover_until)
            )
        else:
            article_count = sites.get_article_count(scraper_queries, site_id)
        return article_count


class SiteLatestArticle(Resource):
    def get(self, site_id):
        latest_article = sites.get_latest_article(scraper_queries, site_id)
        return latest_article


class SitesWarning(Resource):
    def get(self, site_id):
        warning_msg = f"Are you looking for </sites/{site_id}/article_count> or </sites/{site_id}/latest_article>?"
        return {"message": warning_msg}, 404


class PublicationSearch(Resource):
    publications = dict()
    check_points = dict()
    limit = 20
    checkpoint_interval = 3600

    def retrieve_publication(self, pattern):
        last_check_point = self.check_points.get(pattern, 0)
        now = int(time.time())
        if now - last_check_point > self.checkpoint_interval:
            self.publications[pattern] = publications.get_publication(
                pub_queries, pattern
            )
            self.check_points[pattern] = now

        return self.publications[pattern]

    def get(self):
        pattern = request.args.get("q")
        page = request.args.get("page", 1)
        page = int(page)
        matching_publications = self.retrieve_publication(pattern)
        result, status_code = publications.paginate(
            matching_publications, page_requested=page, limit=self.limit
        )
        return result, status_code


class Hello(Resource):
    def get(self):
        welcome_msg = "Hello, welcome to the api of g0v 0archive"
        return {"message": welcome_msg}


api.add_resource(Hello, "/")
api.add_resource(FindArticleByID, "/articles/<int:article_id>")
api.add_resource(FindArticleByURL, "/articles")
api.add_resource(SitesWarning, "/sites/<int:site_id>", "/sites/<int:site_id>/")
api.add_resource(SiteArticleCount, "/sites/<int:site_id>/article_count")
api.add_resource(SiteLatestArticle, "/sites/<int:site_id>/latest_article")
api.add_resource(PublicationSearch, "/publications")

if __name__ == "__main__":
    app.run(debug=True)
