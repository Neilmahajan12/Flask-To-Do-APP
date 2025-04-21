from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, TaskForm
from datetime import datetime
# Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# this is our Models (we can create separate model.py file for this if u  want)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    is_today = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    now = datetime.now()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(owner=current_user).all()
    if form.validate_on_submit():
        new_task = Task(content=form.content.data, owner=current_user)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks, form=form,now=now)

@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You are not authorized to delete this task!', 'danger')
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'info')
    return redirect(url_for('index'))

@app.route('/mark_today/<int:task_id>')
@login_required
def mark_today(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner == current_user:
        task.is_today = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/unmark_today/<int:task_id>')
@login_required
def unmark_today(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner == current_user:
        task.is_today = False
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'warning')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
