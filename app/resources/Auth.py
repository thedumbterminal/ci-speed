from flask_restx import Resource, Namespace
from flask_dance.contrib.github import github
from flask import redirect, url_for


api = Namespace("auth", description="Auth related operations")

def _log_response(resp):
    print(dict(resp.headers))
    print(resp.status_code, resp.json())


@api.route("/login")
class Auth(Resource):
    @api.doc("Login to your account via github")
    def get(self):
        if not github.authorized:
            print('not authorized')
            return redirect(url_for("github.login"))
        resp = github.get("/user")
        _log_response(resp)
        assert resp.ok
        return "You are @{login} on GitHub".format(login=resp.json()["login"])