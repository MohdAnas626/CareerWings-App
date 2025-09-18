from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey123"  

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Haadi7146",
        database="careerwings"
    )
    return conn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        education = request.form["education"]
        skills = request.form["skills"]
        interests = request.form["interests"]
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO users (name, education, skills, interests, username, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, education, skills, interests, username, password))
        conn.commit()
        cursor.close()
        conn.close()

        return "<h2>✅ Registration successful!</h2><a href='/'>Go back to Home</a>"

    return render_template("signup.html")



@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"] 

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        else:
            error = "❌ Invalid username or password."

    return render_template("signin.html", error=error)
    
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin:
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))
        else:
            error = "❌ Invalid username or password."

    return render_template("admin_login.html", error=error)

@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html")

@app.route("/admin_logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("user_login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT name, education, skills, interests
        FROM Users
        WHERE User_ID = %s
    """, (user_id,))
    user = cursor.fetchone()

    conn.close()

    if not user:
        flash("User not found", "danger")
        return redirect(url_for("user_login"))

    return render_template(
        "user_dashboard.html",
        user_name=user["name"],
        education=user["education"],
        skills=user["skills"],
        interests=user["interests"]
    )

@app.route("/user/dashboard")
def user_dashboard():
    if not session.get("user_id"):
        return redirect(url_for("signin"))
    return render_template("user_dashboard.html", section="overview")

@app.route("/user/dashboard/<section>")
def user_dashboard_section(section):
    if not session.get("user_id"):
        return redirect(url_for("signin"))
    return render_template("user_dashboard.html", section=section)  

@app.route("/logout")
def logout():
    session.clear()
    return render_template("goodbye.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
