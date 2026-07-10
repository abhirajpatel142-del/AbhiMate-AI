from dotenv import load_dotenv
load_dotenv()

from flask import jsonify
from payment_verify import verify_payment
from flask import Flask, render_template, request, session, redirect
...
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
from flask import jsonify
from payment_verify import verify_payment
from flask import Flask, render_template, request, session, redirect
from database import db, User, History
from auth import auth
from ai_generator import (
    generate_content,
    generate_script,
    generate_thumbnail,
    generate_hook,
    generate_hashtags
)
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

        history = History(
            username=session["user"],
            topic=topic,
            platform=platform,
            result=result
        )

        db.session.add(history)
        db.session.commit()

        if not user.is_pro:
            user.daily_usage += 1
            db.session.commit()

        with open("outputs/script.txt", "w", encoding="utf-8") as f:
            f.write(result)

        return render_template("index.html", result=result)

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

@app.route("/hook", methods=["POST"])
def hook():

    topic = request.form["topic"]

    result = generate_hook(topic)

    return render_template("index.html", result=result)

@app.route("/hashtags", methods=["POST"])
def hashtags():

    topic = request.form["topic"]

    result = generate_hashtags(topic)

    return render_template("index.html", result=result)

@app.route("/titles", methods=["POST"])
def titles():
    topic = request.form["topic"]

    result = f"""
🔥 10 Viral Titles for "{topic}"

1. {topic} Secret Nobody Told You!
2. Top 5 {topic} Hacks 🤯
3. Don't Make This {topic} Mistake!
4. {topic} Explained in 60 Seconds
5. The Truth About {topic}
6. How to Master {topic} Fast
7. Beginner's Guide to {topic}
8. {topic} Tips That Actually Work
9. Why Everyone Is Talking About {topic}
10. Best {topic} Ideas in 2026
"""

    return render_template("index.html", result=result)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    if user is None:
        session.clear()
        return redirect("/login")

    return render_template("dashboard.html", user=user)

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    items = History.query.filter_by(
        username=session["user"]
    ).order_by(
        History.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        items=items
    )

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

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

@app.route("/payment-success", methods=["POST"])
def payment_success():

    if "user" not in session:
        return jsonify({"success": False})

    data = request.get_json()

    ok = verify_payment(
        data["order_id"],
        data["payment_id"],
        data["signature"]
    )

    if not ok:
        return jsonify({"success": False})

    user = User.query.filter_by(username=session["user"]).first()

    user.is_pro = True
    db.session.commit()

    return jsonify({"success": True})

@app.route("/admin/users")
def admin_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin_users.html", users=users)

@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")

    if session["user"] != "itz__me__abhi_17":
        return "Access Denied", 403

    total_users = User.query.count()
    pro_users = User.query.filter_by(is_pro=True).count()
    total_history = History.query.count()

    users = User.query.order_by(User.id.desc()).all()

    return render_template(
        "admin.html",
        total_users=total_users,
        pro_users=pro_users,
        total_history=total_history,
        users=users
    )

@app.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin")

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/make-pro/<int:user_id>")
def make_pro(user_id):
    user = User.query.get_or_404(user_id)
    user.is_pro = True
    db.session.commit()
    return redirect("/admin")


@app.route("/remove-pro/<int:user_id>")
def remove_pro(user_id):
    user = User.query.get_or_404(user_id)
    user.is_pro = False
    db.session.commit()
    return redirect("/admin")

@app.route("/download/txt")
def download_txt():
    file_path = "outputs/script.txt"

    return send_file(
        file_path,
        as_attachment=True,
        download_name="AbhiMate_AI_Script.txt"
    )


@app.route("/download/pdf")
def download_pdf():
    txt_file = "outputs/script.txt"
    pdf_file = "outputs/script.pdf"

    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph(content.replace("\n", "<br/>"), styles["Normal"])
    )

    doc.build(story)

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="AbhiMate_AI_Script.pdf"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
