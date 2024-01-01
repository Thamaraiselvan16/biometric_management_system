from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "thamarai5118",
    "database": "bms",
}

def connect_to_database():
    return mysql.connector.connect(**db_config)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            query = "SELECT * FROM admin_login WHERE username=%s AND password=%s"
            data = (username, password)

            cursor.execute(query, data)
            user = cursor.fetchone()

            if user:
                return redirect("/admin_home_page")
            else:
                message = "Invalid username. Please try again."
        except mysql.connector.Error as err:
            message = f"Error: {err}"
        finally:
            cursor.close()
            connection.close()

        return render_template("login.html", message=message)

    return render_template("login.html", message="")

@app.route("/registration", methods=["GET"])
def registration_form():
    return render_template("registration.html")

@app.route("/registration", methods=["POST"])
def register_user():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        password = request.form["password"]

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Insert data into the register table
            register_query = "INSERT INTO register (name, phone, password) VALUES (%s, %s, %s)"
            register_data = (name, phone, password)
            cursor.execute(register_query, register_data)

            # Insert data into the emp_login table
            emp_login_query = "INSERT INTO emp_login (employee_username, employee_password) VALUES (%s, %s)"
            emp_login_data = (name, password)
            cursor.execute(emp_login_query, emp_login_data)

            connection.commit()
            # Redirect to the employee home page upon successful registration
            return redirect("/employee")
        except mysql.connector.Error as err:
            message = f"Error: {err}"
        finally:
            cursor.close()
            connection.close()

        return render_template("registration.html", message=message)

@app.route("/employee", methods=["GET", "POST"])
def employee():
    if request.method == "POST":
        employee_username = request.form["employee_username"]
        employee_password = request.form["employee_password"]

        # Validate login credentials from the database
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            query = "SELECT * FROM emp_login WHERE employee_username=%s AND employee_password=%s"
            data = (employee_username, employee_password)

            cursor.execute(query, data)
            user = cursor.fetchone()

            if user:
                return redirect("/emp_home_page")
            else:
                message = "Invalid username. Please try again."
        except mysql.connector.Error as err:
            message = f"Error: {err}"
        finally:
            cursor.close()
            connection.close()

        return render_template("emplogin.html", message=message)

    return render_template("emplogin.html", message="")

@app.route("/admin_home_page")
def admin_home_page():
    return render_template("admin_home_page.html")

@app.route("/emp_home_page")
def emp_home_page():
    return render_template("emp_home_page.html")

if __name__ == "__main__":
    app.run(debug=True)
