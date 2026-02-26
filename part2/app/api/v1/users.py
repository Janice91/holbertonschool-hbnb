from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("users", description="User operations")

user_model = ns.model("User", {
    "first_name": fields.String(required=True, description="First name"),
    "last_name":  fields.String(required=True, description="Last name"),
    "email":      fields.String(required=True, description="Email address")
})

user_response = ns.model("UserResponse", {
    "id":         fields.String(description="User ID"),
    "first_name": fields.String(description="First name"),
    "last_name":  fields.String(description="Last name"),
    "email":      fields.String(description="Email address"),
    "created_at": fields.String(description="Creation date"),
    "updated_at": fields.String(description="Last update date")
})


@ns.route("/")
class UserList(Resource):

    @ns.marshal_list_with(user_response)
    def get(self):
        """List all users (password excluded)"""
        return facade.get_all_users(), 200

    @ns.expect(user_model, validate=True)
    @ns.response(201, "User created successfully")
    @ns.response(400, "Invalid input data")
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(request.json)
            return user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:user_id>")
@ns.param("user_id", "The user identifier")
class UserResource(Resource):

    @ns.response(200, "User found")
    @ns.response(404, "User not found")
    def get(self, user_id):
        """Get a user by ID (password excluded)"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict(), 200

    @ns.expect(user_model, validate=False)
    @ns.response(200, "User updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(404, "User not found")
    def put(self, user_id):
        """Update a user"""
        if not facade.get_user(user_id):
            ns.abort(404, "User not found")
        try:
            updated = facade.update_user(user_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))
