from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from newsSpiders.webapi import sites, articles

app = Flask(__name__)
api = Api(app)


class FindArticleByID(Resource):
    def get(self, article_id):
        result = articles.get_article_by_id(article_id=article_id)
        return jsonify(result)


class FindArticleByURL(Resource):
    def get(self):
        url = request.args.get("url")
        result = articles.get_article_by_url(url)
        return jsonify(result)


class SiteArticleCount(Resource):
    def get(self, site_id):
        article_count = sites.get_article_count(site_id=site_id)
        return jsonify(article_count)


class SiteLatestArticle(Resource):
    def get(self, site_id):
        latest_article = sites.get_latest_article(site_id=site_id)
        return jsonify(latest_article)


api.add_resource(FindArticleByID, "/articles/<int:article_id>")
api.add_resource(FindArticleByURL, "/articles")
api.add_resource(SiteArticleCount, "/sites/<int:site_id>/article_count")
api.add_resource(SiteLatestArticle, "/sites/<int:site_id>/latest_article")


if __name__ == "__main__":
    app.run(debug=True)
