from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login_db"
    )


@app.route("/", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()

        query = """
        SELECT * FROM users
        WHERE username = %s AND password = %s
        """

        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            return render_template(
                "dashboard.html",
                username=username
            )

        message = "Invalid username or password!"

    return render_template(
        "login.html",
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)