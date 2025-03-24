from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anonymous_messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    link_id = db.Column(db.String(64), unique=True)
    messages = db.relationship('Message', backref='recipient', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_link_id(self):
        self.link_id = secrets.token_urlsafe(16)
        return self.link_id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        user.generate_link_id()
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.timestamp.desc()).all()
    unread_count = Message.query.filter_by(user_id=current_user.id, read=False).count()
    share_link = url_for('send_message', link_id=current_user.link_id, _external=True)
    # share_link = url_for('send_message', link_id=current_user.link_id, _external=True, _scheme='https')

    return render_template('dashboard.html', messages=messages, unread_count=unread_count, share_link=share_link)

@app.route('/send/<link_id>', methods=['GET', 'POST'])
def send_message(link_id):
    user = User.query.filter_by(link_id=link_id).first()
    
    if not user:
        abort(404)
    
    if request.method == 'POST':
        content = request.form.get('message')
        
        if content:
            message = Message(content=content, user_id=user.id)
            db.session.add(message)
            db.session.commit()
            flash('Message sent anonymously!')
            return redirect(url_for('send_message', link_id=link_id))
    
    return render_template('send_message.html', username=user.username)

@app.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # Ensure the user can only view their own messages
    if message.user_id != current_user.id:
        abort(403)
    
    # Mark as read if it's not already
    if not message.read:
        message.read = True
        db.session.commit()
    
    return render_template('view_message.html', message=message)

@app.route('/regenerate-link')
@login_required
def regenerate_link():
    current_user.generate_link_id()
    db.session.commit()
    flash('Your anonymous link has been regenerated!')
    return redirect(url_for('dashboard'))

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,ssl_context=('cert.pem', 'key.pem'))

print("Flask application initialized successfully!")