from . import main
from .. import db
from ..models import User, Role
from flask import request, jsonify
from app.auth.views import token_auth

class UserRoutes:
    @main.post("/users")
    def users():
        data = request.get_json()
        new_user = User(
            name = data.get("name"),
            username = data.get("username"),
            email = data.get("email"),
            password = data.get("password"),
            phone_no = data.get("phone_no"),
        )
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": [
            {"data": "User added successfully"},
            {"user": new_user.to_json()}
        ]})
    
    @main.get("/users")
    @token_auth.login_required
    def view_users():
        users = User.query.all()
        users_list = []

        for user in users:
            users_list.append(user.to_json())
        return jsonify({"Users": users_list})
    
    @main.get("/users/<int:id>")
    def view_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        return jsonify(user.to_json())
    
    @main.put("/users/<int:id>")
    def update_user(id):
        data = request.get_json()
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        
        user.name = data.get("name")
        user.username = data.get("username")
        user.email = data.get("email")
        user.phone_no = data.get("phone_no")
        user.role_id = data.get("role_id")

        return jsonify({"message": [
            {"data": "User updated successfully"},
            {"user": user.to_json()}
        ]})
    
    @main.delete("/users/<int:id>")
    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
