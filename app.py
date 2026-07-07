from flask import Flask, render_template, request
from ai_generator import generate_content, generate_script, generate_thumbnail

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":
        topic = request.form["topic"]
        platform = request.form["platform"]
        result = generate_content(topic, platform)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

