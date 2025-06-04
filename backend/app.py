from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from fuzzy_service import analyzer, DEFAULT_CONDITIONS
import os
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  # Vite's default port
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'pilot' or 'passenger'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('userType')

        if not all([email, password, user_type]):
            return jsonify({'error': 'All fields are required'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(email=email, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({
                'message': 'Logged in successfully',
                'userType': user.user_type
            })
        
        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout')
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user')
@login_required
def get_user():
    try:
        return jsonify({
            'email': current_user.email,
            'userType': current_user.user_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-analysis', methods=['GET', 'POST'])
@login_required
def risk_analysis():
    try:
        if request.method == 'POST':
            if current_user.user_type != 'pilot':
                return jsonify({'error': 'Only pilots can update conditions'}), 403
            
            data = request.get_json()
            conditions = {
                'temperature': float(data.get('temperature', DEFAULT_CONDITIONS['temperature'])),
                'humidity': float(data.get('humidity', DEFAULT_CONDITIONS['humidity'])),
                'wind_speed': float(data.get('wind_speed', DEFAULT_CONDITIONS['wind_speed'])),
                'visibility': float(data.get('visibility', DEFAULT_CONDITIONS['visibility']))
            }
        else:
            conditions = DEFAULT_CONDITIONS

        risk_analysis = analyzer.calculate_risks(
            conditions['temperature'],
            conditions['humidity'],
            conditions['wind_speed'],
            conditions['visibility']
        )

        return jsonify(risk_analysis)
    except Exception as e:
        logger.error(f"Error in risk_analysis: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 