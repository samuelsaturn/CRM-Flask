from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Erro na criação do banco de dados: {e}")

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': f'Erro ao obter usuários: {str(e)}'}), 500

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    try:
        new_user = User(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao adicionar usuário. Nome de usuário duplicado: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao adicionar usuário: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
