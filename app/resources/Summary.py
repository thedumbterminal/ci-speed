from flask_restx import Resource, Namespace
from flask_security import auth_required, current_user
from analytics.summary import get_total_test_duration

api = Namespace("summary", description="Summary related operations")


@api.route("/total_test_duration")
class TotalTestDuration(Resource):
    @auth_required("token", "session")
    @api.doc(id="get summary_total_test_duration", security=["apikey"])
    def get(self):
        """Retrieve the total test duration for all projects"""
        return get_total_test_duration(current_user.id)
