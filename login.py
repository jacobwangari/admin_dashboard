from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'your-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Sample user database
users = {
    '1': {'username': 'teacher1', 'password': 'password1', 'role': 'teacher'},
    '2': {'username': 'student1', 'password': 'password1', 'role': 'student'}
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        for user_id, data in users.items():
            if data['username'] == username and data['password'] == password:
                user = User(user_id)
                break

        if user:
            login_user(user)
            return redirect('/dashboard')
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = str(request.args.get('user_id', ''))
    user = users.get(user_id)
    if user:
        if user['role'] == 'teacher':
            return render_template('teacher_dashboard.html', user=user)
        elif user['role'] == 'student':
            return render_template('student_dashboard.html', user=user)
    return 'User not found or invalid role'

if __name__ == '__main__':
    app.run(debug=True)
