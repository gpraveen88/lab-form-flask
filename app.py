from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request
from models import db, Workstation
import requests
import os
from collections import defaultdict
from werkzeug.security import check_password_hash



from datetime import datetime, timedelta
import secrets
from flask import flash, redirect, url_for

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = "PPPAAA@RRRTTT"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwQiFsBus3K7wJkSqLtHeeeMvZFr2TObboA0v85D3BfhP4xUKYY8Qi7CFpGv04tYz_n/exec"

def send_to_google_sheet(data):
    try:
        response = requests.post(
            GOOGLE_SHEET_WEBHOOK_URL,
            json=data,
            timeout=5
        )
        print("✅ Google Sheet updated:", response.text)
    except Exception as e:
        print("❌ Error sending to Google Sheet:", e)

#@app.route("/", methods=["GET", "POST"])
#def index():
#    if request.method == "POST":
#        form_data = request.form.to_dict()
#        room = form_data.get("room_lab_name")
#        cubicle = form_data.get("cubicle_no")

        # ✅ Check for existing assignment of same room + cubicle
 #       existing = Workstation.query.filter_by(room_lab_name=room, cubicle_no=cubicle).first()
  #      if existing:
   #         error_msg = f"⚠️ Cubicle {cubicle} in {room} has already been assigned."
    #        return render_template("index.html", error=error_msg, form_data=form_data)
#
        # ✅ No conflict — proceed to save
 #       workstation = Workstation(**form_data)
  #      db.session.add(workstation)
   #     db.session.commit()

    #    send_to_google_sheet(form_data)
     #   return "✅ Submitted Successfully"

 #   return render_template("index.html")
#

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login_home")
@login_required
def login_home():
    return render_template("login_home.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    error = None
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        room = form_data.get("room_lab_name")
        cubicle = form_data.get("cubicle_no")
        roll = form_data.get("roll")

        # ✅ Check if roll number already exists
        existing_roll = Workstation.query.filter_by(roll=roll).first()
        if existing_roll:
            error = f"⚠️ Roll number {roll} has already been allotted a machine."
            return render_template("index.html", error=error, form_data=form_data)

        # ✅ Check if cubicle in lab is already assigned
        existing_cubicle = Workstation.query.filter_by(room_lab_name=room, cubicle_no=cubicle).first()
        if existing_cubicle:
            error = f"⚠️ Cubicle {cubicle} in {room} has already been assigned."
            return render_template("index.html", error=error, form_data=form_data)

        # ✅ Save the new entry
        workstation = Workstation(**form_data)
        db.session.add(workstation)
        db.session.commit()

        send_to_google_sheet(form_data)
        return "✅ Submitted Successfully"

    return render_template("index.html")

@app.route("/records")
def view_records():
    all_records = Workstation.query.all()

    # Lab-wise capacity definition
    lab_capacities = {
        "CS-107": 43,
        "CS-108": 21,
        "CS-109": 114,
        "CS-207": 30,
        "CS-208": 25,
        "CS-209": 142,
        "CS-317": 25,
        "CS-318": 25,
        "CS-319": 32,
        "CS-320": 27,
        "CS-411": 25,
        "CS-412": 33
    }

    from collections import defaultdict
    grouped_records = defaultdict(list)

    # Group records by lab
    for r in all_records:
        grouped_records[r.room_lab_name].append(r)

    # Calculate stats per lab
    lab_stats = {}
    for lab, records in grouped_records.items():
        total = lab_capacities.get(lab, 0)
        used = len(records)
        available = total - used
        lab_stats[lab] = {"total": total, "used": used, "available": available}

    # Sort labs by name
    grouped_records = dict(sorted(grouped_records.items()))

    return render_template("records.html", grouped_records=grouped_records, lab_stats=lab_stats)

from flask_login import login_required, current_user

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    result = None
    message = None

    if request.method == "POST":
        roll = request.form.get("roll")
        result = Workstation.query.filter_by(roll=roll).first()
        if not result:
            message = f"No machine has been allocated for Roll Number: {roll}"

    return render_template("search.html", result=result, message=message, layout="login_home.html")

@app.route("/utilization")
def utilization():
    all_records = Workstation.query.all()

    lab_capacities = {
        "CS-107": 43,
        "CS-108": 21,
        "CS-109": 114,
        "CS-207": 30,
        "CS-208": 25,
        "CS-209": 142,
        "CS-317": 25,
        "CS-318": 25,
        "CS-319": 32,
        "CS-320": 27,
        "CS-411": 25,
        "CS-412": 33
    }

    from collections import defaultdict
    lab_counts = defaultdict(int)
    for r in all_records:
        lab_counts[r.room_lab_name] += 1

    lab_stats = {}
    for lab, total in lab_capacities.items():
        used = lab_counts.get(lab, 0)
        available = total - used
        lab_stats[lab] = {
            "total": total,
            "used": used,
            "available": available
        }

    return render_template("utilization.html", lab_stats=lab_stats)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("⚠️ Email already registered. Please login.", "warning")
            return redirect("/login")

        hashed_pw = generate_password_hash(password)

        # ✅ Auto-approve if email is admin
        is_admin = email.lower() == "admin@cse.iith.ac.in"

        user = User(email=email, password=hashed_pw, is_approved=is_admin)
        db.session.add(user)
        db.session.commit()

        flash("✅ Registered!" + (" You're auto-approved as Admin." if is_admin else " Please wait for admin approval."))
        return redirect("/login")

    return render_template("register.html")

from flask import flash, redirect, url_for
from flask_login import login_user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if not user.is_approved:
                flash("⚠️ Awaiting admin approval.")
                return redirect(url_for("login"))
            login_user(user)
            flash("✅ Logged in successfully.")
            return redirect(url_for("login_home"))
        else:
            flash("❌ Invalid credentials.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/reset-request", methods=["GET", "POST"])
def reset_request():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(16)
            user.reset_token = token
            user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
            db.session.commit()
            # In production, send email. Here, show URL
            flash(f"Reset link: http://127.0.0.1:5006/reset-password/{token}")
        else:
            flash("Email not found")
        return redirect(url_for("reset_request"))
    return render_template("reset_request.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        return "Invalid or expired token"

    if request.method == "POST":
        new_password = request.form.get("password")
        user.password = generate_password_hash(new_password)  # ✅ hash password
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        flash("Password updated! You can now log in.")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/admin/approve")
@login_required
def approve_panel():
    if current_user.email != "admin@cse.iith.ac.in":
        return "Access Denied"
    pending_users = User.query.filter_by(is_approved=False).all()
    return render_template("approve_users.html", users=pending_users)


@app.route("/admin/approve/<int:user_id>")
@login_required
def approve_user(user_id):
    if current_user.email != "admin@cse.iith.ac.in":
        return "Access Denied"
    user = User.query.get(user_id)
    if user:
        user.is_approved = True
        db.session.commit()
    return redirect(url_for("approve_panel"))


@app.route("/admin/reject/<int:user_id>")
@login_required
def reject_user(user_id):
    if current_user.email != "admin@cse.iith.ac.in":
        return "Access Denied"
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("approve_panel"))

from flask_login import current_user

@app.route("/cse_labs")
def cse_labs():
    layout_template = "login_home.html" if current_user.is_authenticated else "base.html"
    return render_template("cse_labs.html", layout=layout_template)

@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

from flask_login import login_required, current_user

@app.route("/inventory", methods=["GET"])
@login_required
def inventory():
    return render_template("inventory.html", layout="login_home.html")

if __name__ == "__main__":
    app.run(debug=True, port=5009)
