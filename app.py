import sqlite3
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        course = request.form["course"]
        age = request.form["age"]

        connection = sqlite3.connect("students.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students(name, course, age)
            VALUES (?, ?, ?)
            """,
            (name, course, age)
        )

        connection.commit()
        connection.close()

        return f"""
        <h1>Student Added!</h1>

        {name} has been added successfully.

        <br><br>

        <a href="/">🏠 Home</a>

        <br><br>

        <a href="/students">📋 View Students</a>
        """

    return render_template("add_student.html")

@app.route("/students")

def students():

    connection = sqlite3.connect("students.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return render_template(
        "students.html",
        students=students
    )

@app.route("/delete/<int:id>")
def delete_student(id):

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/students")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        course = request.form["course"]
        age = request.form["age"]

        cursor.execute(
            """
            UPDATE students
            SET name=?, course=?, age=?
            WHERE id=?
            """,
            (name, course, age, id)
        )

        connection.commit()
        connection.close()

        return redirect("/students")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_student.html",
        student=student
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)