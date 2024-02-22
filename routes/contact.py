from flask import render_template, Blueprint

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact-us")
def contact_us():
    return render_template("contact_us.html")
