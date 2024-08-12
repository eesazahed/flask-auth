from cs50 import SQL
from flask import Flask, render_template, request

db = SQL("sqlite:///database.db")
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, password)

        return render_template("registered.html", username=username)

    return render_template("register.html")


@app.route("/getusers")
def getusers():
    users = db.execute("SELECT * FROM users")

    return { "data": users }


if __name__ == "__main__":
    app.run()