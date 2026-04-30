from datetime import datetime
from app import db, bcrypt

# Association table: users <-> projects (team members)
project_members = db.Table(
    "project_members",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="Member")  # Admin / Member
    designation = db.Column(db.String(80), default="Team Member")  # e.g., "Senior Developer"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owned_projects = db.relationship("Project", backref="owner", lazy=True, foreign_keys="Project.owner_id")
    assigned_tasks = db.relationship("Task", backref="assignee", lazy=True, foreign_keys="Task.assignee_id")
    progress_reports = db.relationship("ProgressReport", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_performance(self):
        """Calculate user performance score in real-time"""
        from app.models import Task  # avoid circular import
        # Query fresh from DB to get latest data
        user_tasks = Task.query.filter_by(assignee_id=self.id).all()
        total = len(user_tasks)
        if total == 0:
            return {"total": 0, "completed": 0, "in_progress": 0, "overdue": 0, "score": 0, "completion_rate": 0}
        completed = sum(1 for t in user_tasks if t.status == "Done")
        in_progress = sum(1 for t in user_tasks if t.status == "In Progress")
        overdue = sum(1 for t in user_tasks if t.is_overdue())
        score = completed * 10 + in_progress * 3 - overdue * 2
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "overdue": overdue,
            "score": max(score, 0),
            "completion_rate": round((completed / total) * 100, 1),
        }

    def to_dict(self, include_perf=False):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "designation": self.designation,
            "created_at": self.created_at.isoformat(),
        }
        if include_perf:
            data["performance"] = self.get_performance()
        return data


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    phase = db.Column(db.String(50), default="Planning")  # Planning / Development / Testing / Deployment / Completed
    progress = db.Column(db.Integer, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="project", lazy=True, cascade="all, delete-orphan")
    members = db.relationship("User", secondary=project_members, backref="projects")
    reports = db.relationship("ProgressReport", backref="project", lazy=True, cascade="all, delete-orphan")

    def is_overdue(self):
        return self.due_date and self.due_date < datetime.utcnow() and self.phase != "Completed"

    def days_remaining(self):
        if not self.due_date:
            return None
        delta = (self.due_date - datetime.utcnow()).days
        return delta

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner.to_dict() if self.owner else None,
            "members": [m.to_dict() for m in self.members],
            "task_count": len(self.tasks),
            "completed_tasks": sum(1 for t in self.tasks if t.status == "Done"),
            "phase": self.phase,
            "progress": self.progress,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "days_remaining": self.days_remaining(),
            "is_overdue": self.is_overdue(),
            "created_at": self.created_at.isoformat(),
        }


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="Todo")
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_overdue(self):
        return self.due_date and self.due_date < datetime.utcnow() and self.status != "Done"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project_id": self.project_id,
            "project_name": self.project.name if self.project else None,
            "assignee": self.assignee.to_dict() if self.assignee else None,
            "overdue": self.is_overdue(),
            "created_at": self.created_at.isoformat(),
        }


class ProgressReport(db.Model):
    __tablename__ = "progress_reports"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    progress_percentage = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user": self.user.to_dict() if self.user else None,
            "content": self.content,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat(),
        }