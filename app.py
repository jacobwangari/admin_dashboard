from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:PassWord%40123@localhost/chesingele"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adm = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)
    
    def __init__(self,adm,name,phone,password,role):
        self.adm = adm
        self.name = name
        self.phone = phone
        self.password = password
        self.role = role
        
        
# # Create an application context
# with app.app_context():
#   # Create the database tables
#   db.create_all()  
    

@app.route('/')
def home():
    
    all_data = Users.query.all()
    return render_template('index.html', users = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        adm = request.form['adm']
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role']
        
        user = Users(adm,name,phone,password,role)
        db.session.add(user)
        db.session.commit()
        
        flash("User created sucessfully")
        
        return redirect(url_for('home'))
    
@app.route('/update', methods = ['GET','POST'])
def update():
    data = Users.query.get(request.form.get('id'))
    if request.method == 'POST':
        data.adm = request.form['adm']
        data.name = request.form['name']
        data.phone = request.form['phone']
        data.password = request.form['password']
        data.role = request.form['role']
        
        db.session.commit()
        
        flash("User updated sucessfully")
        
        return redirect(url_for('home'))
    
@app.route('/delete/<id>/', methods = ['GET','POST'])
def delete(id):
    data_ = Users.query.get(id)
    db.session.delete(data_)
    db.session.commit()
        
    flash("User deleted sucessfully")
        
    return redirect(url_for('home'))
    
        
    


if(__name__ == "__main__"):
    app.run(debug = True)
    