from flask import Flask, render_template, request, session, redirect
from database import db, User
from auth import auth
from ai_generator import generate_content, generate_script, generate_thumbnail
from payment import create_order

app = Flask(__name__)

app.config["SECRET_KEY"] = "abhimate-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///abhimate.db"

db.init_app(app)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    if user is None:
        session.clear()
        return redirect("/login")

    if not user.is_pro and user.daily_usage >= 3:
        return redirect("/pricing")

    result = ""

    if request.method == "POST":
        topic = request.form["topic"]
        platform = request.form["platform"]

        result = generate_content(topic, platform)

        if not user.is_pro:
            user.daily_usage += 1
            db.session.commit()

    return render_template("index.html", result=result)


@app.route("/script", methods=["POST"])
def script():
    topic = request.form["topic"]
    result = generate_script(topic)
    return render_template("index.html", result=result)


@app.route("/thumbnail", methods=["POST"])
def thumbnail():
    topic = request.form["topic"]
    result = generate_thumbnail(topic)
    return render_template("index.html", result=result)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/buy-pro")
def buy_pro():
    if "user" not in session:
        return redirect("/login")

    order = create_order()

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"]
    }

@app.route("/payment-success")
def payment_success():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    if user:
        user.is_pro = True
        db.session.commit()

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
