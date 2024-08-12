from cs50 import SQL
from flask import Flask, render_template, request, redirect
import jwt
import os

secret = os.environ["secret"]

db = SQL("sqlite:///database.db")
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

app = Flask(__name__)

def checkIfUsernameExists(username):
    user = db.execute(f"SELECT * FROM users WHERE username='{username}'")

    if user:
        return True
    else:
        return False

def checkUsernameAndPassword(username, password):
    user = db.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")

    if user:
        return True
    else:
        return False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if checkIfUsernameExists(username):
            return render_template("unavailableusername.html", username=username) 

        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, password)

        return render_template("registered.html", username=username)

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if checkIfUsernameExists(username) == False:
            return render_template("userdoesntexist.html", username=username) 

        if checkUsernameAndPassword(username, password) == False:
            return render_template("incorrectlogininfo.html") 

        encoded_jwt = jwt.encode({ "username": username}, secret, algorithm="HS256")

        return render_template("loggedin.html", username=username, jwt=encoded_jwt)

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    token = request.cookies.get("jwt")

    if token:
        try:
            data = jwt.decode(token, secret, algorithms=["HS256"])
            return render_template("dashboard.html", username=data.username) 
        except jwt.ExpiredSignatureError:
            return "Token has expired", 401
        except jwt.InvalidTokenError:
            return "Invalid token", 401
    return redirect("/login")


@app.route("/getusers")
def getusers():
    users = db.execute("SELECT DISTINCT username FROM users")

    return { "data": users }


if __name__ == "__main__":
    app.run()