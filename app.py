from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wayne.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'funcionario', 'gerente', 'admin'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120))
    status = db.Column(db.String(50), default='disponivel')  # disponivel, em_uso, manutenção
    notes = db.Column(db.Text)

# Utilities
def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)

def requires_login(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify({'error':'unauthorized'}), 401
        return f(*args, **kwargs)
    return wrapper

def requires_role(*roles):
    def deco(f):
        from functools import wraps
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user or user.role not in roles:
                return jsonify({'error':'forbidden'}), 403
            return f(*args, **kwargs)
        return wrapper
    return deco

# Routes - Frontend
@app.route('/')
def index():
    user = current_user()
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return render_template('login.html', error='Credenciais inválidas')
    session.permanent = True
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Endpoints
@app.route('/api/me')
def api_me():
    user = current_user()
    if not user:
        return jsonify({'user': None})
    return jsonify({'user': {'id':user.id,'username':user.username,'role':user.role}})

@app.route('/api/resources', methods=['GET','POST'])
@requires_login
def api_resources():
    if request.method == 'GET':
        q = Resource.query.all()
        out = []
        for r in q:
            out.append({'id':r.id,'name':r.name,'type':r.type,'location':r.location,'status':r.status,'notes':r.notes})
        return jsonify(out)
    data = request.json
    user = current_user()
    if user.role not in ('gerente','admin'):
        return jsonify({'error':'forbidden'}), 403
    r = Resource(name=data.get('name'), type=data.get('type') or 'desconhecido', location=data.get('location'), status=data.get('status','disponivel'), notes=data.get('notes'))
    db.session.add(r)
    db.session.commit()
    return jsonify({'id': r.id}), 201

@app.route('/api/resources/<int:rid>', methods=['GET','PUT','DELETE'])
@requires_login
def api_resource_detail(rid):
    r = Resource.query.get_or_404(rid)
    user = current_user()
    if request.method == 'GET':
        return jsonify({'id':r.id,'name':r.name,'type':r.type,'location':r.location,'status':r.status,'notes':r.notes})
    if request.method == 'DELETE':
        if user.role != 'admin':
            return jsonify({'error':'forbidden'}), 403
        db.session.delete(r)
        db.session.commit()
        return jsonify({'deleted': True})
    # PUT (update)
    if user.role not in ('gerente','admin'):
        return jsonify({'error':'forbidden'}), 403
    data = request.json
    r.name = data.get('name', r.name)
    r.type = data.get('type', r.type)
    r.location = data.get('location', r.location)
    r.status = data.get('status', r.status)
    r.notes = data.get('notes', r.notes)
    db.session.commit()
    return jsonify({'updated': True})

@app.route('/api/stats')
@requires_login
def api_stats():
    total = Resource.query.count()
    by_status = {}
    for s in ('disponivel','em_uso','manutencao'):
        by_status[s] = Resource.query.filter_by(status=s).count()
    return jsonify({'total_resources': total, 'by_status': by_status})

# CLI helper: initialize DB
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    if not os.path.exists('wayne.db'):
        db.create_all()
    app.run(debug=True)
