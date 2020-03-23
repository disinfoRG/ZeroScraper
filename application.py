from flask import Flask, request
from flask_restful import Resource, Api
import pugsql
import os
import time
from dotenv import load_dotenv
from newsSpiders.webapi import sites, articles, publications, stats

app = Flask(__name__)
api = Api(app)

load_dotenv()
# scraper db
scraper_queries = pugsql.module("queries/")
scraper_queries.connect(os.getenv("DB_URL"))
# publication db
pub_queries = pugsql.module("queries/parser")
pub_queries.connect(os.getenv("PUB_DB_URL"))


class GetArticleByID(Resource):
    def get(self, article_id):
        result = articles.get_article_by_id(scraper_queries, article_id)
        return result


class GetArticleByURL(Resource):
    def get(self):
        url = request.args.get("url")
        result = articles.get_article_by_url(scraper_queries, url)
        if "error_message" in result[0].keys():
            return result, 404
        return result


class GetActiveSites(Resource):
    def get(self):
        result = sites.get_active_sites(scraper_queries)
        return result


class GetSiteNewArticles(Resource):
    def get(self, site_id):
        now = int(time.time())
        time_start = request.args.get("timeStart", 0)
        time_end = request.args.get("timeEnd", now)
        result = sites.get_articles_discovered_in_interval(
            scraper_queries, site_id, int(time_start), int(time_end)
        )
        return result


class GetSiteUpdatedArticles(Resource):
    def get(self, site_id):
        now = int(time.time())
        time_start = request.args.get("timeStart", 0)
        time_end = request.args.get("timeEnd", now)
        result = sites.get_articles_updated_in_interval(
            scraper_queries, site_id, int(time_start), int(time_end)
        )
        return result


class GetSiteLatestArticle(Resource):
    def get(self, site_id):
        latest_article = sites.get_latest_article(scraper_queries, site_id)
        return latest_article


class SitesWarning(Resource):
    def get(self, site_id):
        warning_msg = f"Are you looking for </sites/{site_id}/article_count> or </sites/{site_id}/latest_article>?"
        return {"message": warning_msg}, 404


class GetStats(Resource):
    def get(self):
        site_id = request.args.get("site_id", None)
        date = request.args.get("date", None)
        if site_id:
            site_id = int(site_id)
            result = stats.get_stats_by_site(scraper_queries, site_id=site_id)
        elif date:
            result = stats.get_stats_by_date(scraper_queries, date=date)
        else:
            result = stats.get_all_stats(scraper_queries)
        return result


class SearchPublication(Resource):
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
api.add_resource(GetArticleByID, "/articles/<int:article_id>")
api.add_resource(GetArticleByURL, "/articles")
api.add_resource(SitesWarning, "/sites/<int:site_id>", "/sites/<int:site_id>/")
api.add_resource(GetSiteNewArticles, "/sites/<int:site_id>/new_articles")
api.add_resource(GetSiteUpdatedArticles, "/sites/<int:site_id>/updated_articles")
api.add_resource(GetSiteLatestArticle, "/sites/<int:site_id>/latest_article")
api.add_resource(GetActiveSites, "/sites/active")
api.add_resource(GetStats, "/stats")
api.add_resource(SearchPublication, "/publications")

if __name__ == "__main__":
    app.run(debug=True)
