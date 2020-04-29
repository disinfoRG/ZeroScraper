from flask import request
from flask_jwt_extended import create_access_token


def post_login(api_password):
    username = request.values.get("username")
    password = request.values.get("password")
    if not password or not username:
        body = {"message": "Missing username or password."}
        return {"body": body, "status_code": 400}

    if password != api_password:
        body = {"message": f"Wrong password."}
        return {"body": body, "status_code": 401}

    access_token = create_access_token(identity=username, expires_delta=False)
    body = {
        "message": "Login successfully.",
        "access_token": access_token,
    }
    return {"body": body, "status_code": 200}
