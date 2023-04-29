from flask_restx import Resource, Namespace
from flask_dance.contrib.github import github
from flask import redirect, url_for


api = Namespace("login", description="Login related operations")


def _log_response(resp):
    print(dict(resp.headers))
    print(resp.status_code, resp.json())


@api.route("/")
class Login(Resource):
    @api.doc(id="login")
    def get(self):
        """Login to your account via github"""
        try:
            if github.authorized:
                resp = github.get("/user")
                _log_response(resp)
                assert resp.ok
                return "You are @{login} on GitHub".format(login=resp.json()["login"])
        except ValueError as e:
            print("Error from authorized()", e)
        print("Not authorised with GitHub")
        return redirect(url_for("github.login"))
