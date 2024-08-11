from flask_restx import Resource, Namespace
from db.models import Waypoint as Model
from schemas import WaypointSchema as ModelSchema
from flask_security import auth_required

api = Namespace("waypoints", description="Waypoint related operations")


@api.route("/<int:waypoint_id>")
@api.param("waypoint_id", "The waypoint identifier")
class Waypoint(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_waypoint", security=["apikey"])
    def get(self, suite_id):
        """Retrieve a waypoint"""
        result = Model.query.get(suite_id)
        model_schema = ModelSchema()
        return model_schema.dump(result)
