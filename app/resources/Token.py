from flask_restx import Resource, Namespace
from flask_security import auth_required, current_user


api = Namespace("token", description="Token related operations")


def _log_response(resp):
    print(dict(resp.headers))
    print(resp.status_code, resp.json())


@api.route("/")
class Token(Resource):
    @auth_required("session")
    @api.doc("Generate/regenerate an auth token of the current user")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def post(self):
        """Generate/regenerate an auth token"""
        return {"token": current_user.get_auth_token()}
