import os
import pugsql
from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    set_access_cookies,
    unset_access_cookies,
    get_jwt_identity,
    jwt_optional,
)

from newsSpiders.webapi import (
    sites,
    articles,
    publications,
    stats,
    monitor,
    auth,
    playground,
)
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("API_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ("headers", "cookies")
app.config["JWT_ACCESS_COOKIE_PATH"] = [
    "/articles",
    "/sites",
    "/stats",
    "/publications",
]
jwt = JWTManager(app)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10/second"])

# scraper db
scraper_queries = pugsql.module("queries/")
scraper_queries.connect(os.getenv("DB_URL"))
# playground db
playground_queries = pugsql.module("queries/playground")
playground_queries.connect(os.getenv("PLAY_DB_URL"))


response_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Content-Type": "application/json",
}

api_password = os.getenv("API_PASSWORD")


def create_response(body, status_code=200, headers=dict()):
    if isinstance(body, list):
        body = jsonify(body)
    resp = make_response(body, status_code, response_headers)
    resp.headers.update(headers)
    return resp


@app.route("/", methods=["GET"])
@jwt_optional
def hello():
    username = get_jwt_identity()
    if username:
        welcome_msg = f"Hello {username}, welcome to the api of g0v 0archive"
    else:
        welcome_msg = "Hello, welcome to the api of g0v 0archive, please login first."
    return create_response(welcome_msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        headers = {"Content-Type": "text/html"}
        return create_response(render_template("login_form.html"), 200, headers)
    else:
        result = auth.post_login(api_password)
        access_token = result["body"].get("access_token")
        response = create_response(**result)
        if access_token:
            set_access_cookies(response, access_token)
        return response


@app.route("/logout", methods=["GET", "POST"])
def logout():
    response = create_response("Logout successfully.")
    unset_access_cookies(response)

    return response


@app.route("/health", methods=["GET"])
def check_health():
    result = monitor.check_health(scraper_queries)
    return create_response(**result)


@app.route("/variables", methods=["GET"])
@jwt_required
def get_variable():
    result = monitor.get_variables(scraper_queries, request.args)
    return create_response(**result)


@app.route("/articles", methods=["GET"])
@jwt_required
def get_articles():
    result = articles.get_articles(scraper_queries, request.args)
    return create_response(**result)


@app.route("/articles/<int:article_id>", methods=["GET"])
@jwt_required
def get_article_by_id(article_id):
    result = articles.get_article_by_id(scraper_queries, article_id)
    return create_response(**result)


@app.route("/sites", methods=["GET"])
@jwt_required
def get_sites():
    result = sites.get_sites(scraper_queries, request.args)
    return create_response(**result)


@app.route("/sites/active", methods=["GET"])
@jwt_required
def get_active_sites():
    result = sites.get_active_sites(scraper_queries)
    return create_response(**result)


@app.route("/sites/<int:site_id>", methods=["GET"])
@jwt_required
def get_site_by_id(site_id):
    result = sites.get_site_by_id(scraper_queries, site_id)
    return create_response(**result)


@app.route("/sites/<int:site_id>/article_count", methods=["GET"])
@jwt_required
def get_site_article_count(site_id):
    result = sites.get_article_count(scraper_queries, site_id)
    return create_response(**result)


@app.route("/sites/<int:site_id>/latest_article", methods=["GET"])
@jwt_required
def get_site_latest_article(site_id):
    result = sites.get_latest_article(scraper_queries, site_id)
    return create_response(**result)


@app.route("/stats", methods=["GET"])
@jwt_required
def get_stats():
    result = stats.get_stats(scraper_queries, request.args)
    return create_response(**result)


@app.route("/publications", methods=["GET"])
@jwt_required
def search_publication():
    result = publications.search_publication(os.getenv("PUB_SEARCH_URL"), request.args)
    return create_response(**result)


@app.route("/playground/random", methods=["GET"])
def get_random_title():
    result = playground.get_random_title(playground_queries)
    return create_response(**result)


@app.route("/playground/add_record", methods=["POST"])
def post_token():
    result = playground.add_record(playground_queries)
    return create_response(**result)


if __name__ == "__main__":
    app.run(debug=True)
