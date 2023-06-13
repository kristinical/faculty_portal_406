# ***************************************************************
#  Author: Kristin Eberman                                      *
#  Independent Project: Education Expeditions Faculty Portal    *
#  CS406 | Spring 2023 | Oregon State University                *
#                                                               *  
#  CODE CITATION:                                               *
#  This code is based on OSU's CS340 Flask-Starter-App          *
#  URL: https://github.com/osu-cs340-ecampus/flask-starter-app  *
# ***************************************************************

from flask import Flask, render_template, request, redirect, json, session, send_from_directory
from flask_mysqldb import MySQL
from flask_session import Session
import os, operator
import database.db_connector as db
db_connection = db.connect_to_database()


# Configure Flask app and set secret key
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = 'not the real key'


# configure connection to database (actual names and password are removed)
app.config['MYSQL_HOST'] = 'db_host_name'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


# Route for Login page to Portal
@app.route('/')
def root():
    return render_template("login.html")


# Route for Logout (reset session variables)
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect("/")


# Route to validate login credentials
@app.route('/portal', methods=['POST'])
def portal_login():
    # Get form data entered by user
    username = request.form.get('username')
    password = request.form.get('password')

    # Use helper method to validate login credentials
    result = validateLogin(username, password)

    # False result means invalid login attempt
    if result is False:
        return render_template("invalid_login.html")
    
    # True means user is an Admin; activate Admin session
    elif result is True:
        session['admin'] = True
        return redirect("/admin")

    # otherwise user is Faculty; activate Faculty session
    else:
        session['faculty'] = result
        return redirect("/faculty")


# Route for Faculty Portal page
# ******************************************************************************************
#  CODE CITATION: Sort a list of dictionaries by a dictionary value 
#  COPYRIGHT: PythonHow / ACCESSED: June 6, 2023                    
#  URL: https://pythonhow.com/how/sort-a-list-of-dictionaries-by-a-value-of-the-dictionary/   
# ******************************************************************************************
@app.route('/faculty')
def faculty_portal():
    # return to login page if no Faculty session is active
    programID = session.get('faculty', 0)
    if not programID or programID == -1:
        return redirect("/")

    # use helper functions to get program info and task list
    program = get_program_info(int(programID))
    tasks = get_tasks(int(programID))

    # display portal page for program connected to the Faculty User
    return render_template("faculty.html", program=program, tasks=tasks)


# Route to display sample program document
# *****************************************************************
#  CODE CITATION: How to Open a PDF File on the Browser with Flask    
#  POSTED BY: Wallace on January 2, 2021 / ACCESSED: June 6, 2023
#  URL: https://artsysops.com/2021/01/02/how-to-open-a-pdf-file-on-the-browser-with-flask/   
# *****************************************************************
@app.route('/view')
def view_document():
    # Retrieve file path to display (PDF opens in a new tab)
    dir = os.path.abspath(os.getcwd())
    filepath = dir + '/static/'
    return send_from_directory(filepath, 'Sample_Program_Document.pdf')


# Route to upload document
@app.route('/upload', methods=["POST"])
def upload():
    # Retrieve taskID so DB can be updated
    taskID = request.form.get("taskID")
    return render_template("upload.html", task=taskID)
        

# Route to submit upload
@app.route('/submit', methods=["POST"])
def submit():
    # Ensure programID session value is saved
    programID = session.get('faculty', 0)
    session['faculty'] = programID

    # Update DB by marking task as complete
    taskID = request.form.get('taskID')
    update_task = "UPDATE Tasks SET completed = 1 WHERE taskID = '%d'" % int(taskID)
    db.execute_query(db_connection=db_connection, query=update_task)
    return redirect('/faculty')
        

# Route for Admin Portal homepage
@app.route('/admin')
def admin_portal():
    # return to login page if Admin session is not active
    admin = session.get('admin', 0)
    if not admin:
        return redirect('/')

    # run SQL query to get list of programs (for dropdown menu on Admin homepage)
    programs_query = "SELECT programID, destination, programName FROM Programs"
    cursor = db.execute_query(db_connection=db_connection, query=programs_query)
    json_result = json.dumps(cursor.fetchall())
    program_list = json.loads(json_result)

    # sort programs by due date
    sorted_programs = sorted(program_list, key=operator.itemgetter('destination'))
    return render_template("admin.html", programs=sorted_programs)


# Route for Admin Portal program page
@app.route('/program', methods=['GET', 'POST'])
def program_page():
    # return to Login page if Admin session is not active
    admin = session.get('admin', 0)
    if not admin:
        return redirect('/')

    # activate Admin Program session
    if request.method == "POST":
        programID = request.form.get('programs')
        session['program'] = programID

    # return to Admin homepage if no program is selected
    programID = session.get('program', 0)
    if not programID:
        return redirect('/admin')

    # use helper functions to get program info and task list
    program = get_program_info(int(programID))
    tasks = get_tasks(int(programID))

    return render_template("program.html", program=program, tasks=tasks, programID=programID)


# Route to delete a Task from Program
@app.route('/delete', methods=["POST"])
def delete():
    # Ensure programID session value is saved
    programID = session.get('program', 0)
    session['program'] = programID

    # Delete task from DB
    taskID = request.form.get('delete')
    delete_task = "DELETE FROM Tasks WHERE taskID = '%d'" % int(taskID)
    db.execute_query(db_connection=db_connection, query=delete_task)
    
    return redirect('/program')


# Routes to add a Task to a Program
@app.route('/add', methods=["POST"])
def add():
    programID = request.form.get('add')
    program = get_program_info(int(programID))
    return render_template("add.html", program=program)

@app.route('/add_task', methods=["POST"])
def add_task():
    # Ensure programID session value is saved
    programID = session.get('program', 0)
    session['program'] = programID

    # Parse user input from form
    taskName = request.form.get('taskName')
    taskType = request.form.get('taskType')
    dueDate = request.form.get('dueDate')

    # Insert task into DB
    add_task = "INSERT INTO Tasks (taskName, taskType, dueDate, programID) VALUES ('%s', '%s', '%s', '%d')" % (taskName, taskType, dueDate, int(programID))
    db.execute_query(db_connection=db_connection, query=add_task)

    return redirect('/program')


# Routes to edit a Task in a Program
@app.route('/edit', methods=["POST"])
def edit():
    # Get program info to display in table
    programID = session.get('program', 0)
    program = get_program_info(int(programID))

    # Get Task info from DB
    taskID = request.form.get('edit')
    query = "SELECT * FROM Tasks WHERE taskID = '%d'" % (int(taskID))
    cursor = db.execute_query(db_connection=db_connection, query=query)
    json_result = json.dumps(cursor.fetchall())
    task = json.loads(json_result)[0]
    print(task)

    return render_template("edit.html", program=program, task=task, taskType=task['taskType'], taskID=taskID)

@app.route('/edit_task', methods=["POST"])
def edit_task():
    # Ensure programID session value is saved
    programID = session.get('program', 0)
    session['program'] = programID

    # Parse user input from form
    taskName = request.form.get('taskName')
    taskType = request.form.get('taskType')
    dueDate = request.form.get('dueDate')
    completed_val = request.form.get('completed')
    taskID = request.form.get('taskID')

    if completed_val == "No":
        completed = 0
    elif completed_val == "Yes":
        completed = 1


    # Edit task in DB
    edit_task = "UPDATE Tasks SET taskName = '%s', taskType = '%s', dueDate = '%s', completed = '%d' WHERE taskID = '%d'" % (taskName, taskType, dueDate, completed, int(taskID))
    db.execute_query(db_connection=db_connection, query=edit_task)

    return redirect('/program')


# function that validates login credentials and determines if user is Admin or Faculty
def validateLogin(username, password):
    # run SQL query against username (form input)
    query = "SELECT * FROM Users WHERE username = '%s'" % (username)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    json_result = json.dumps(cursor.fetchall())
    result = json.loads(json_result)

    # return False if result is empty (no username matched)
    if result == []:
        return False
    
    elif result[0]['password'] != password:
        return False
    
    # return True if user is an Admin
    elif result[0]['admin'] == 1:
        return True

    # otherwise return the programID of Faculty user
    else:
        return result[0]['programID']


# function that returns Program Info from DB in list form
def get_program_info(programID):
    # run SQL query against programID to get program info   
    program_query = "SELECT * FROM Programs WHERE programID = '%d'" % (programID)
    cursor = db.execute_query(db_connection=db_connection, query=program_query)
    json_result = json.dumps(cursor.fetchall())
    result = json.loads(json_result)
    program = result[0]

    # format dates to MM/DD/YYYY format
    startDate = program["startDate"].split('-')
    program["startDate"] = f"{startDate[1]}/{startDate[2]}/{startDate[0]}"

    endDate = program["endDate"].split('-')
    program["endDate"] = f"{endDate[1]}/{endDate[2]}/{endDate[0]}"

    return program


# function that returns Program Tasks in a sorted list by due date
def get_tasks(programID):
    # run SQL query against programID to get program tasks
    task_query = "SELECT * FROM Tasks WHERE programID = '%d'" % (programID)
    cursor = db.execute_query(db_connection=db_connection, query=task_query)
    json_result = json.dumps(cursor.fetchall())
    task_list = json.loads(json_result)

    # format due date to MM/DD/YYYY format
    for task in task_list:
        dueDate = task["dueDate"].split('-')
        task["dueDate"] = f"{dueDate[1]}/{dueDate[2]}/{dueDate[0]}"
    
    # sort tasks by due date
    return sorted(task_list, key=operator.itemgetter('dueDate'))


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9875))
    app.run(port=port, debug=False) 
