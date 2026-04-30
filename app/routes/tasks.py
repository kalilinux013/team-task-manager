from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Task, Project, User
from app.decorators import get_current_user

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.get("/")
@jwt_required()
def list_tasks():
    user = get_current_user()
    project_id = request.args.get("project_id", type=int)
    q = Task.query
    if project_id:
        q = q.filter_by(project_id=project_id)
    if user.role != "Admin":
        # only tasks in projects user belongs to
        ids = [p.id for p in user.projects + user.owned_projects]
        q = q.filter(Task.project_id.in_(ids))
    return jsonify([t.to_dict() for t in q.all()])


@tasks_bp.post("/")
@jwt_required()
def create_task():
    user = get_current_user()
    data = request.get_json() or {}
    project = Project.query.get_or_404(data.get("project_id"))

    if user.role != "Admin" and user not in project.members:
        return jsonify({"error": "Forbidden"}), 403

    due = data.get("due_date")
    task = Task(
        title=data.get("title", "").strip(),
        description=data.get("description", ""),
        status=data.get("status", "Todo"),
        priority=data.get("priority", "Medium"),
        due_date=datetime.fromisoformat(due) if due else None,
        project_id=project.id,
        assignee_id=data.get("assignee_id"),
    )
    if not task.title:
        return jsonify({"error": "Title required"}), 400
    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)  # Force reload from DB
    return jsonify(task.to_dict())


@tasks_bp.patch("/<int:tid>")
@jwt_required()
def update_task(tid):
    user = get_current_user()
    task = Task.query.get_or_404(tid)

    if user.role != "Admin" and user not in task.project.members:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    for f in ("title", "description", "status", "priority"):
        if f in data:
            setattr(task, f, data[f])
    if "due_date" in data and data["due_date"]:
        task.due_date = datetime.fromisoformat(data["due_date"])
    if "assignee_id" in data:
        task.assignee_id = data["assignee_id"]
    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.delete("/<int:tid>")
@jwt_required()
def delete_task(tid):
    user = get_current_user()
    task = Task.query.get_or_404(tid)
    if user.role != "Admin" and task.project.owner_id != user.id:
        return jsonify({"error": "Forbidden"}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Deleted"})