from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["IMDbProject"]
collection = db["authentication"]

app = Flask(__name__)


@app.route("/")
def func():
    return render_template("index.html")


@app.route("/signed")
def success():
    email = request.args.get("sign_email")
    password = request.args.get("sign_password")
    if email and password:
        collection.insert_one({"email": email, "password": password})
        return render_template("success.html")
    if not email:
        return render_template("email_failure.html")
    if not password:
        return render_template("password_failure.html")


@app.route("/logged")
def log():
    email = request.args.get("log_email")
    password = request.args.get("log_password")
    user = collection.find_one({"email": email, "password": password})
    if user:
        return render_template("main.html")
    return render_template("invalid_user.html")


if __name__ == "__main__":
    app.run(debug=True)

