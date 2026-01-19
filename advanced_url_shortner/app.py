from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import string, random, validators

from models import db, User, URL

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/dashboard")
        flash("Invalid username or password")
    return render_template("login.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 and 9 characters")
            return redirect("/signup")

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect("/signup")

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully")
        return redirect("/")
    return render_template("signup.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form["url"]

        if not validators.url(original_url):
            error = "Invalid URL format"
        else:
            code = generate_short_code()
            new_url = URL(
                original_url=original_url,
                short_code=code,
                user_id=current_user.id
            )
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + code

    return render_template("dashboard.html", short_url=short_url, error=error)

# ---------------- HISTORY ----------------
@app.route("/history")
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", urls=urls)

# ---------------- REDIRECT ----------------
@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
