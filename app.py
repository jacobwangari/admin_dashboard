from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:PassWord%40123@localhost/chesingele"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    class_name = db.Column(db.String(255))
    body = db.Column(db.Text)

    def __init__(self, title, subject, class_name, body):
        self.title = title
        self.subject = subject
        self.class_name = class_name
        self.body = body
    
    def __repr__(self):
        return f"Assignment(id={self.id}, title='{self.title}', subject='{self.subject}', class_name='{self.class_name}', body='{self.body}')"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adm = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)
    
    def __init__(self, adm, name, phone, password, role):
        self.adm = adm
        self.name = name
        self.phone = phone
        self.set_password(password)
        self.role = role
        
    @staticmethod
    def authenticate(adm, password):
        user = Users.query.filter_by(adm=adm).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


# Routes of the app
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/academics")
def academics():
    return render_template('academics.html')

@app.route("/news")
def news():
    return render_template('news.html')

@app.route("/activities")
def activities():
    return render_template('activities.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        class_name = request.form['class']
        body = request.form['body']
        date = datetime.utcnow()

        assignment = Assignment(title=title, subject=subject, class_name=class_name, body=body)
        db.session.add(assignment)
        db.session.commit()

        flash("Assignment added successfully")

        return redirect(url_for('dashboard'))

    return render_template('add_assignment.html')

@app.route("/assignments")
def assignments():
    assignments = Assignment.query.all() 
    return render_template('assignments.html', assignments = assignments)

@app.route('/assignment/<int:assignment_id>')
def display_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    return render_template('assignment.html', assignments=assignment)
    



@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        adm = request.form['adm']
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role']
        
        user = Users(adm, name, phone, password, role)
        db.session.add(user)
        db.session.commit()
        
        flash("User created successfully")
        
        return redirect(url_for('dashboard'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    data = Users.query.get(request.form.get('id'))
    if request.method == 'POST':
        data.adm = request.form['adm']
        data.name = request.form['name']
        data.phone = request.form['phone']
        data.password = request.form['password']
        data.role = request.form['role']
        
        db.session.commit()
        
        flash("User updated successfully")
        
        return redirect(url_for('dashboard'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data_ = Users.query.get(id)
    db.session.delete(data_)
    db.session.commit()
        
    flash("User deleted successfully")
        
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        adm = request.form['adm']
        password = request.form['password']

        user = Users.query.filter_by(adm=adm).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        
        flash('Invalid adm or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the user ID from the session
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get the user ID from the session
    user_id = session['user_id']

    # Get the user from the database
    user = Users.query.get(user_id)
    assignments = Assignment.query.all() 

    if user.role == 'admin':
        # Logic for admin dashboard
        all_data = Users.query.all()
        return render_template('admin_dashboard.html',user= user, users=all_data)
    elif user.role == 'teacher':
        # Logic for teacher dashboard
        return render_template('teacher_dashboard.html', user=user, assignments = assignments)
    elif user.role == 'student':
        # Logic for student dashboard
        return render_template('student_dashboard.html', user=user, assignments = assignments)
    else:
        flash('Invalid user role')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
