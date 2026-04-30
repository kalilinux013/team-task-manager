from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("login.html")

@dashboard_bp.route("/signup")
def signup_page():
    return render_template("signup.html")

@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")