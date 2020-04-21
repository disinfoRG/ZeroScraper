import os
import time

import pugsql
from flask import Flask, request, make_response, jsonify, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    set_access_cookies, unset_access_cookies, get_jwt_identity, jwt_optional
)
from flask_restful import Resource, Api

from newsSpiders.webapi import sites, articles, publications, stats, monitor

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("API_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ('headers', 'cookies')
app.config['JWT_ACCESS_COOKIE_PATH'] = ['/articles', '/sites', '/stats', '/publications']
jwt = JWTManager(app)
api = Api(app)

# scraper db
scraper_queries = pugsql.module("queries/")
scraper_queries.connect(os.getenv("DB_URL"))
# publication db
pub_queries = pugsql.module("queries/parser")
pub_queries.connect(os.getenv("PUB_DB_URL"))

response_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true"
}


def create_response(body, status_code=200, headers=None):
    if isinstance(body, list):
        body = jsonify(body)
    resp = make_response(body, status_code, response_headers)
    if headers:
        resp.headers.update(headers)
    return resp


class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return create_response(render_template('login_form.html'), 200, headers)

    def post(self):
        username = request.args.get('username') or request.form.get('username')
        password = request.args.get('password') or request.form.get('password')

        if not password or not username:
            body = {"message": "Missing username or password."}
            return create_response(body, 400)

        if password != os.getenv("API_PASSWORD"):
            body = {"message": f"Wrong password"}
            return create_response(body, 401)

        access_token = create_access_token(identity=username, expires_delta=False)
        response = create_response({"access-token": access_token})
        set_access_cookies(response, access_token)

        return response


class Logout(Resource):
    def post(self):
        response = create_response({"message": "Logout successful."})
        unset_access_cookies(response)

        return response


@app.route('/health', methods=["GET"])
def check_health():
    result = monitor.check_health(scraper_queries)
    return create_response(**result)


@app.route('/variable', methods=["GET"])
@jwt_required
def get_variable():
    result = monitor.get_variable(scraper_queries)
    return create_response(**result)


@app.route('/article/<int:article_id>', methods=["GET"])
@jwt_required
def get_article_by_id(article_id):
    result = articles.get_article_by_id(scraper_queries, article_id)
    return create_response(**result)


@app.route('/article', methods=["GET"])
@jwt_required
def get_article_by_url():
    result = articles.get_article_by_url(scraper_queries)
    return create_response(**result)


@app.route('/sites', methods=["GET"])
@jwt_required
def get_all_sites():
    result = sites.get_all_sites(scraper_queries)
    return create_response(**result)


@app.route('/sites/active', methods=["GET"])
@jwt_required
def get_active_sites():
    result = sites.get_active_sites(scraper_queries)
    return create_response(**result)


@app.route('/sites/<int:site_id>/new_articles', methods=["GET"])
@jwt_required
def get_articles_discovered_in_interval(site_id):
    result = sites.get_articles_discovered_in_interval(scraper_queries, site_id)
    return create_response(**result)


@app.route('/sites/<int:site_id>/updated_articles', methods=["GET"])
@jwt_required
def get_articles_updated_in_interval(site_id):
    result = sites.get_articles_updated_in_interval(scraper_queries, site_id)
    return create_response(**result)


@app.route('/stats', methods=["GET"])
@jwt_required
def get_stats():
    result = stats.get_stats(scraper_queries)
    return create_response(**result)


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

    @jwt_required
    def get(self):
        pattern = request.args.get("q")
        page = request.args.get("page", 1)
        page = int(page)
        matching_publications = self.retrieve_publication(pattern)
        result, status_code = publications.paginate(
            matching_publications, page_requested=page, limit=self.limit
        )
        return result, status_code


@app.route('/', methods=["GET"])
@jwt_optional
def hello():
    username = get_jwt_identity()
    if username:
        welcome_msg = f"Hello {username}, welcome to the api of g0v 0archive"
    else:
        welcome_msg = "Hello, welcome to the api of g0v 0archive, please login first."
    return create_response({"message": welcome_msg})


api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(SearchPublication, "/publications")

if __name__ == "__main__":
    app.run(debug=True)
