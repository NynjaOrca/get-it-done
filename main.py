from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done-now:nynja@localhost:8889/get-it-done-now'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "y337kGcys&zP3B"

# -------------------------------------------------------------------------------

class Task(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    desc = db.Column(db.String(500))
    completed = db.Column(db.Boolean)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.completed = False

# -------------------------------------------------------------------------------

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# -------------------------------------------------------------------------------

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        task_desc = request.form['desc']
        if not task_name or not task_desc:
            return redirect('/')
        else:
            new_task = Task(task_name, task_desc)
            db.session.add(new_task)
            db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

# -------------------------------------------------------------------------------

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/')
        else:
            # TODO - failed login line
            return '<h1>ERROR</h1>'

    return render_template('login.html')

# -------------------------------------------------------------------------------

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        email_error = ''
        password_error = ''
        verify_error = ''
        

        upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        special = "!@#$%^&*?"

        # email
        at_count = 0
        e_space_count = 0
        dot_count = 0

        # password
        upper_count = 0
        p_space_count = 0
        digit_count = 0
        special_count = 0
        char_count = 0


#        for char in str(email):
#            if char == '@':
#                at_count += 1
#            elif char == ' ':
#                e_space_count += 1
#            elif char == '.':
#                dot_count += 1

#        if not (at_count == 1) or not (e_space_count == 0) or not (dot_count >= 1):
#            email_error += "invalid email address"
        
#        for char in str(password):
#            char_count += 1

#            if char in upper_alpha:
#                upper_count += 1
#            elif char in digits:
#                digit_count += 1
#            elif char == ' ':
#                p_space_count += 1
#            elif char in special:
#                special_count += 1

#        if not upper_count >= 1:
#            password_error += "Password must contain an upper-case character"
#        elif not digit_count >= 1:
#            password_error += "Password must contain a digit"
#        elif not special_count >= 1:
#            password_error += "Password must contain a special character"
#        elif not p_space_count == 0:
#            password_error += "Password must not contain whitespace"
#        elif (len(password) < 3) or (len(password) > 20):
#            password_error += "Password must be between 3 and 20 characters"

#        if verify != password:
#            verify_error += 'Your passwords did not match'

        registered_user = User.query.filter_by(email=email).first()
        if not email_error and not password_error and not verify_error and not registered_user:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return render_template('register.html', email_error=email_error, password_error=password_error, verify_error=verify_error)

    return render_template('register.html')

# -------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

# -------------------------------------------------------------------------------

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect('/')

# -------------------------------------------------------------------------------

@app.route('/complete-task', methods=['POST'])
def complete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

# -------------------------------------------------------------------------------

@app.before_request
def require_login():
    allowed_routes = ['register', 'login']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()