from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("users", description="User operations")

user_model = ns.model("User", {
    "first_name": fields.String(required=True),
    "last_name":  fields.String(required=True),
    "email":      fields.String(required=True),
    "is_admin":   fields.Boolean(default=False)
})


@ns.route("/")
class UserList(Resource):

    def get(self):
        """List all users"""
        return [u.to_dict() for u in facade.get_all_users()], 200

    @ns.expect(user_model, validate=True)
    def post(self):
        """Create a user"""
        try:
            user = facade.create_user(request.json)
            return user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:user_id>")
class UserResource(Resource):

    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict(), 200

    @ns.expect(user_model, validate=False)
    def put(self, user_id):
        """Update a user"""
        if not facade.get_user(user_id):
            ns.abort(404, "User not found")
        try:
            updated = facade.update_user(user_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))
