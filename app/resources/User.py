from flask_restx import Resource, Namespace
from flask_security import auth_required, current_user
from schemas import UserSchema


api = Namespace("user", description="User related operations")


def _log_response(resp):
    print(dict(resp.headers))
    print(resp.status_code, resp.json())


@api.route("/")
class User(Resource):
    @auth_required("token", "session")
    @api.doc("Get the info of the current user")
    # @api.doc(security=['apikey', {'oauth2': ['read']}])
    @api.doc(security=["apikey"])
    def get(self):
        """Retrieve the current user"""
        user_schema = UserSchema()
        return user_schema.dump(current_user)
