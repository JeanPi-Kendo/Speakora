from flask import Blueprint, render_template, request

practice_bp = Blueprint("practice", __name__)


@practice_bp.route("/practice")
def practice():
    language = request.args.get("language")  # viene del botón del formulario
    return render_template("practice/select_level.html", language=language)
