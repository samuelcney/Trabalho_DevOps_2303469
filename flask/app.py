from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@mariadb/students_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

# Modelo de Aluno
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ra = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)

# Inicialização do banco de dados
@app.before_first_request
def init_db():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_student():
    data = request.get_json()
    ra = data.get('ra')
    name = data.get('name')
    if not ra or not name:
        return jsonify({"error": "RA and name are required"}), 400

    student = Student(ra=ra, name=name)
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"}), 201

@app.route('/students', methods=['GET'])
def list_students():
    students = Student.query.all()
    return jsonify([{"id": student.id, "ra": student.ra, "name": student.name} for student in students])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

