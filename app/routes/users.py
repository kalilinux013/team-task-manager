from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from email_validator import validate_email, EmailNotValidError
from app import db
from app.models import User
from app.decorators import get_current_user, admin_required

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
@jwt_required()
def list_users():
    """All authenticated users can list (needed for member assignment dropdowns)"""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict(include_perf=True) for u in users])


@users_bp.post("/")
@admin_required
def create_user():
    """Admin creates a new user account"""
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "Member")
    designation = data.get("designation", "Team Member")

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be 6+ characters"}), 400
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"error": "Invalid email"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    if role not in ("Admin", "Member"):
        role = "Member"

    user = User(name=name, email=email, role=role, designation=designation)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.patch("/<int:uid>")
@admin_required
def update_user(uid):
    """Admin updates user role/designation/name"""
    user = User.query.get_or_404(uid)
    data = request.get_json() or {}
    if "role" in data and data["role"] in ("Admin", "Member"):
        user.role = data["role"]
    if "designation" in data:
        user.designation = data["designation"]
    if "name" in data:
        user.name = data["name"]
    db.session.commit()
    return jsonify(user.to_dict())


@users_bp.delete("/<int:uid>")
@admin_required
def delete_user(uid):
    """Admin deletes a user (cannot delete other admins or self)"""
    current = get_current_user()
    if current.id == uid:
        return jsonify({"error": "Cannot delete yourself"}), 400
    user = User.query.get_or_404(uid)
    if user.role == "Admin":
        return jsonify({"error": "Admin users are protected and cannot be deleted"}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Deleted"})


@users_bp.get("/leaderboard")
@jwt_required()
def leaderboard():
    """Performance leaderboard with top performer badge"""
    users = User.query.all()
    data = []
    for u in users:
        d = u.to_dict(include_perf=True)
        data.append(d)
    data.sort(key=lambda x: x["performance"]["score"], reverse=True)
    for i, u in enumerate(data):
        if i == 0 and u["performance"]["score"] > 0:
            u["badge"] = "🏆 Top Performer"
        elif i == 1 and u["performance"]["score"] > 0:
            u["badge"] = "🥈 Runner Up"
        elif i == 2 and u["performance"]["score"] > 0:
            u["badge"] = "🥉 Bronze"
        else:
            u["badge"] = None
    return jsonify(data)