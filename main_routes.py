# app/routes/main_routes.py
from flask import Blueprint, render_template

# Definimos el blueprint principal
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")
