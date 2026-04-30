from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Project, User, ProgressReport
from app.decorators import get_current_user, admin_required

projects_bp = Blueprint("projects", __name__)

@projects_bp.get("/")
@jwt_required()
def list_projects():
    user = get_current_user()
    if user.role == "Admin":
        projects = Project.query.all()
    else:
        projects = list(set(user.projects + user.owned_projects))
    return jsonify([p.to_dict() for p in projects])


@projects_bp.get("/<int:pid>")
@jwt_required()
def get_project(pid):
    user = get_current_user()
    project = Project.query.get_or_404(pid)
    if user.role != "Admin" and user not in project.members and project.owner_id != user.id:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(project.to_dict())


@projects_bp.post("/")
@admin_required
def create_project():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Project name required"}), 400

    user = get_current_user()
    project = Project(
        name=name,
        description=data.get("description", ""),
        owner_id=user.id,
        phase=data.get("phase", "Planning"),
    )
    if data.get("start_date"):
        project.start_date = datetime.fromisoformat(data["start_date"])
    if data.get("due_date"):
        project.due_date = datetime.fromisoformat(data["due_date"])

    project.members.append(user)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@projects_bp.patch("/<int:pid>")
@jwt_required()
def update_project(pid):
    user = get_current_user()
    project = Project.query.get_or_404(pid)

    if user.role != "Admin" and project.owner_id != user.id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    for f in ("name", "description", "phase"):
        if f in data:
            setattr(project, f, data[f])
    if "progress" in data:
        project.progress = max(0, min(100, int(data["progress"])))
    if "start_date" in data and data["start_date"]:
        project.start_date = datetime.fromisoformat(data["start_date"])
    if "due_date" in data and data["due_date"]:
        project.due_date = datetime.fromisoformat(data["due_date"])
    db.session.commit()
    return jsonify(project.to_dict())


# ============== MEMBER MANAGEMENT ==============
@projects_bp.post("/<int:pid>/members")
@admin_required
def add_member(pid):
    project = Project.query.get_or_404(pid)
    data = request.get_json() or {}
    user_id = data.get("user_id")
    email = data.get("email", "").lower()

    member = None
    if user_id:
        member = User.query.get(user_id)
    elif email:
        member = User.query.filter_by(email=email).first()

    if not member:
        return jsonify({"error": "User not found"}), 404
    if member in project.members:
        return jsonify({"error": "User already a member"}), 409

    project.members.append(member)
    db.session.commit()
    return jsonify(project.to_dict())


@projects_bp.delete("/<int:pid>/members/<int:uid>")
@admin_required
def remove_member(pid, uid):
    project = Project.query.get_or_404(pid)
    member = User.query.get_or_404(uid)
    if member in project.members:
        project.members.remove(member)
        db.session.commit()
    return jsonify(project.to_dict())


@projects_bp.delete("/<int:pid>")
@admin_required
def delete_project(pid):
    project = Project.query.get_or_404(pid)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ============== PROGRESS REPORTS ==============
@projects_bp.get("/<int:pid>/reports")
@jwt_required()
def list_reports(pid):
    user = get_current_user()
    project = Project.query.get_or_404(pid)
    if user.role != "Admin" and user not in project.members:
        return jsonify({"error": "Forbidden"}), 403
    reports = ProgressReport.query.filter_by(project_id=pid).order_by(ProgressReport.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reports])


@projects_bp.post("/<int:pid>/reports")
@jwt_required()
def add_report(pid):
    user = get_current_user()
    project = Project.query.get_or_404(pid)
    if user.role != "Admin" and user not in project.members:
        return jsonify({"error": "You must be a project member"}), 403

    data = request.get_json() or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Report content required"}), 400

    pct = max(0, min(100, int(data.get("progress_percentage", 0))))
    report = ProgressReport(
        project_id=pid,
        user_id=user.id,
        content=content,
        progress_percentage=pct,
    )
    # Auto-update project progress to highest reported
    if pct > project.progress:
        project.progress = pct
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201


# ============== NOTIFICATIONS / ALERTS ==============
@projects_bp.get("/alerts")
@jwt_required()
def get_alerts():
    """Returns due-soon and overdue projects/tasks for the current user"""
    user = get_current_user()
    if user.role == "Admin":
        projects = Project.query.all()
    else:
        projects = list(set(user.projects + user.owned_projects))

    alerts = []
    for p in projects:
        if p.phase == "Completed":
            continue
        days = p.days_remaining()
        if days is None:
            continue
        if days < 0:
            alerts.append({
                "type": "overdue",
                "severity": "high",
                "project_id": p.id,
                "title": p.name,
                "message": f"Project overdue by {abs(days)} day(s)",
                "days": days,
            })
        elif days <= 3:
            alerts.append({
                "type": "due_soon",
                "severity": "medium",
                "project_id": p.id,
                "title": p.name,
                "message": f"Due in {days} day(s)",
                "days": days,
            })
        elif days <= 7:
            alerts.append({
                "type": "upcoming",
                "severity": "low",
                "project_id": p.id,
                "title": p.name,
                "message": f"Due in {days} days",
                "days": days,
            })
    return jsonify(alerts)